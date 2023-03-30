import pandas as pd
import numpy
import sklearn
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.model_selection import cross_validate
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
from joblib import dump
import xgboost as xgb
from sklearn.metrics import accuracy_score
# import packages for hyperparameters tuning
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
import sklearn.metrics as metrics
import numpy as np


def mean_score(scoring):
    return {i: j.mean() for i, j in scoring.items()}


def evaluate_model(model, x_test, y_test):
    # Predict Test Data
    y_pred = model.predict(x_test)

    # Calculate accuracy, precision, recall, f1-score, and kappa score
    acc = metrics.accuracy_score(y_test, y_pred)
    prec = metrics.precision_score(y_test, y_pred)
    rec = metrics.recall_score(y_test, y_pred)
    f1 = metrics.f1_score(y_test, y_pred)
    kappa = metrics.cohen_kappa_score(y_test, y_pred)

    # Calculate area under curve (AUC)
    y_pred_proba = model.predict_proba(x_test)[::, 1]
    fpr, tpr, _ = metrics.roc_curve(y_test, y_pred_proba)
    auc = metrics.roc_auc_score(y_test, y_pred_proba)
    # Display confusion matrix
    cm = metrics.confusion_matrix(y_test, y_pred)

    return {'acc': acc, 'prec': prec, 'rec': rec, 'f1': f1, 'kappa': kappa,
            'fpr': fpr, 'tpr': tpr, 'auc': auc, 'cm': cm}


def plot_confusion_matrix(cm,name,title):
    # Plot the confusion matrix as a bar graph
    fig, ax = plt.subplots()
    im = ax.imshow(cm, cmap='Blues')

    # Add labels to the plot
    ax.set_xticks(np.arange(2))
    ax.set_yticks(np.arange(2))
    ax.set_xticklabels(['Predicted benign', 'Predicted Phishing'])
    ax.set_yticklabels(['Actual benign', 'Actual Phishing'])

    # Add annotations to the cells
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center", color="black")

    # Display the plot
    plt.title(title)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.savefig(name)
    # plt.show()


def plot_roc(fpr, tpr, roc_auc,name,title):
    plt.figure()
    plt.plot(fpr, tpr, color='red', label='AUC = %0.2f)' % roc_auc)
    plt.xlim((0, 1))
    plt.ylim((0, 1))
    plt.plot([0, 1], [0, 1], color="navy", linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.legend(loc='lower right')
    plt.savefig(name)
    # plt.show()


if __name__ == '__main__':

    df = pd.read_csv("../data_collection/training_dataset.csv", )

    df = sklearn.utils.shuffle(df)
    X = df.drop("Result", axis=1).values
    X = preprocessing.scale(X)
    mapping = {-1: 1, 1: 0}
    df = df.replace({"Result": mapping})
    y = df['Result'].values

    # split in 80% train and 20% final testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, shuffle=True)

    # Check if ratio of -1 and 1 is equal between train and test set
    unique, counts = numpy.unique(y_test, return_counts=True)
    percentages = dict(zip(unique, counts * 100 / len(y_test)))
    print(percentages)
    unique, counts = numpy.unique(y_train, return_counts=True)
    percentages = dict(zip(unique, counts * 100 / len(y_train)))
    print(percentages)

    scoring = {'accuracy': 'accuracy',
               'recall': 'recall',
               'precision': 'precision',
               'f1': 'f1'}
    fold_count = 10

    space = {'max_depth': hp.quniform("max_depth", 3, 18, 1),
             'gamma': hp.uniform('gamma', 1, 9),
             'reg_alpha': hp.quniform('reg_alpha', 40, 180, 1),
             'reg_lambda': hp.uniform('reg_lambda', 0, 1),
             'colsample_bytree': hp.uniform('colsample_bytree', 0.5, 1),
             'min_child_weight': hp.quniform('min_child_weight', 0, 10, 1),
             'n_estimators': 180,
             'seed': 0
             }


    def objective(space):
        clf = xgb.XGBClassifier(early_stopping_rounds=10, eval_metric="auc",
                                n_estimators=space['n_estimators'], max_depth=int(space['max_depth']),
                                gamma=space['gamma'],
                                reg_alpha=int(space['reg_alpha']), reg_lambda=int(space['reg_lambda']), min_child_weight=int(space['min_child_weight']),
                                colsample_bytree=int(space['colsample_bytree']))

        evaluation = [(X_train, y_train), (X_test, y_test)]

        clf.fit(X_train, y_train,eval_set=evaluation,
                verbose=False)
        pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, pred > 0.5)
        print("SCORE:", accuracy)
        return {'loss': -accuracy, 'status': STATUS_OK}


    trials = Trials()

    best_hyperparams = fmin(fn=objective,
                            space=space,
                            algo=tpe.suggest,
                            max_evals=200,
                            trials=trials)

    print("The best hyperparameters are : ", "\n")
    print(best_hyperparams)

    space = best_hyperparams
    xgb_clf = xgb.XGBClassifier(n_estimators=180, max_depth=int(space['max_depth']),
                            gamma=space['gamma'],
                            reg_alpha=int(space['reg_alpha']), reg_lambda=int(space['reg_lambda']) ,min_child_weight=int(space['min_child_weight']),
                            colsample_bytree=int(space['colsample_bytree']))
    xgb_clf.fit(X_train, y_train)
    xg_eval = evaluate_model(xgb_clf,X_test,y_test)

    cross_val_scores = cross_validate(xgb_clf, X, y, cv=fold_count, scoring=scoring)
    XGB_clf_score = mean_score(cross_val_scores)

    plot_confusion_matrix(xg_eval['cm'],"confusion_matrix_xgb.png","Confusion Matrix XGB")
    plot_roc(xg_eval['fpr'],xg_eval['tpr'],xg_eval['auc'],"roc_curve_xgb.png","ROC curve XGB")

    dump(xgb_clf, "tuned_phishing_xgb_model.joblib")

    ##### MLP CLASSIFIER ##########################################################

    solvers = ['lbfgs', 'adam', 'sgd']
    learning_rates = ['constant', 'invscaling', 'adaptive']
    activations = ['identity', 'logistic', 'tanh', 'relu']
    space = {'solver': hp.choice('solver', solvers),
             'alpha': hp.uniform('alpha', 0, 1),
             'learning_rate': hp.choice('learning_rate', learning_rates),
             'activation': hp.choice('activation', activations)
             }

    def objective(space):
        clf = MLPClassifier(hidden_layer_sizes=(33,), early_stopping=True, max_iter=500, solver=space["solver"],
                            alpha=space["alpha"], learning_rate=space["learning_rate"])

        clf.fit(X_train, y_train)
        pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, pred > 0.5)
        print("SCORE:", accuracy)
        return {'loss': -accuracy, 'status': STATUS_OK}

    trials = Trials()

    best_hyperparams = fmin(fn=objective,
                            space=space,
                            algo=tpe.suggest,
                            max_evals=200,
                            trials=trials)
    print(best_hyperparams)

    space = best_hyperparams
    mlp_clf = MLPClassifier(hidden_layer_sizes=(33,), max_iter=500, solver=solvers[space['solver']], alpha=space['alpha'],
                            learning_rate=learning_rates[space['learning_rate']],
                            activation=activations[space['activation']])
    mlp_clf.fit(X_train, y_train)
    mlp_eval = evaluate_model(mlp_clf, X_test, y_test)

    cross_val_scores = cross_validate(mlp_clf, X, y, cv=fold_count, scoring=scoring)
    MLP_clf_score = mean_score(cross_val_scores)

    plot_confusion_matrix(mlp_eval['cm'],"confusion_matrix_mlp.png","Confusion Matrix MLP")
    plot_roc(mlp_eval['fpr'], mlp_eval['tpr'], mlp_eval['auc'],"roc_curve_mlp.png","ROC curve MLP")

    dump(mlp_clf, "tuned_phishing_MLP_model.joblib")

    print("####### XGBoost Classifier #######")
    print('Accuracy:', xg_eval['acc'])
    print('Precision:', xg_eval['prec'])
    print('Recall:', xg_eval['rec'])
    print('F1 Score:', xg_eval['f1'])
    print('Cohens Kappa Score:', xg_eval['kappa'])
    print('Area Under Curve:', xg_eval['auc'])
    print('Confusion Matrix:\n', xg_eval['cm'])

    print("####### MLP Classifier #######")
    print('Accuracy:', mlp_eval['acc'])
    print('Precision:', mlp_eval['prec'])
    print('Recall:', mlp_eval['rec'])
    print('F1 Score:', mlp_eval['f1'])
    print('Cohens Kappa Score:', mlp_eval['kappa'])
    print('Area Under Curve:', mlp_eval['auc'])

    print("XGB cross validate scores:")
    print(XGB_clf_score)
    print("MLP cross validate scores:")
    print(MLP_clf_score)

    # # Best parameter set
    # print('Best parameters found:\n', clf.best_params_)
    #
    # # All results
    # means = clf.cv_results_['mean_test_score']
    # stds = clf.cv_results_['std_test_score']
    # for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    #     print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
    #
    # y_true, y_pred = y_test, clf.predict(X_test)
    #
    # plot_confusion_matrix(y_test,y_pred)
    # print('Results on the test set:')
    # print(classification_report(y_true, y_pred))

    # Save model in a joblib file to load whenever necessary
    # dump(clf,"tuned_phishing_model.joblib")
