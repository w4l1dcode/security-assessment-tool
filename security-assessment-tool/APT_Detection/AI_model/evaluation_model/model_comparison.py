# Import the necessary libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from keras.layers import Input, Dense
from keras.models import Model
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

# Load the data from the CSV file
data = pd.read_csv('../../data_collection/trainings_data.csv')

# Split the data into features and labels
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Scale the data
sc = StandardScaler()
X = sc.fit_transform(X)

# Split the data into training, validation, and testing sets
X_train, X_val_test, y_train, y_val_test = train_test_split(X, y, test_size=0.2, random_state=0)
X_val, X_test, y_val, y_test = train_test_split(X_val_test, y_val_test, test_size=0.5, random_state=0)

# Convert data into numpy arrays
X_train = np.array(X_train)
y_train = np.array(y_train)
X_test = np.array(X_test)
y_test = np.array(y_test)

# Create the encoding layer
encoding_dim1 = 60
encoding_dim2 = 35
encoding_dim3 = 20
input_layer = Input(shape=(X_train.shape[1],))
# "encoded" is the encoded representation of the input
encoded = Dense(encoding_dim1, activation='relu')(input_layer)
encoded = Dense(encoding_dim2, activation='relu')(encoded)
encoded = Dense(encoding_dim3, activation='relu')(encoded)
# Create the decoding layer
decoded = Dense(encoding_dim2, activation='relu')(encoded)
decoded = Dense(encoding_dim1, activation='relu')(decoded)
decoded = Dense(X_train.shape[1], activation='sigmoid')(decoded)

# Create the autoencoder model
autoencoder = Model(input_layer, decoded)

# Compile the autoencoder model
autoencoder.compile(optimizer='adam', loss='mean_squared_error')

# Train the autoencoder model
autoencoder.fit(X_train, X_train, epochs=10, batch_size=10, shuffle=False, validation_data=(X_val, X_val))

# Create the encoding model
encoder = Model(input_layer, encoded)

# Encode the data
encoded_train = encoder.predict(X_train)
encoded_test = encoder.predict(X_test)

# Train a classifier on the encoded data
#classifier = tree.DecisionTreeClassifier(random_state=0)
#classifier.fit(encoded_train, y_train)

# Building Decision Tree model
dtc = tree.DecisionTreeClassifier(random_state=0)
dtc.fit(X_train, y_train)

# Building Random Forest model
rf = RandomForestClassifier(random_state=0)
rf.fit(X_train, y_train)

# Building Naive Bayes model
nb = GaussianNB()
nb.fit(X_train, y_train)

# Building KNN model
knn = KNeighborsClassifier()
knn.fit(encoded_train, y_train)


def evaluate_model(model, x_test, y_test):
    from sklearn import metrics
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
    # Display confussion matrix
    cm = metrics.confusion_matrix(y_test, y_pred)
    return {'acc': acc, 'prec': prec, 'rec': rec, 'f1': f1, 'kappa': kappa,
            'fpr': fpr, 'tpr': tpr, 'auc': auc, 'cm': cm}


# Evaluate Model
dtc_eval = evaluate_model(dtc, encoded_test, y_test)
# Evaluate Model
rf_eval = evaluate_model(rf, encoded_test, y_test)
# Evaluate Model
nb_eval = evaluate_model(nb, encoded_test, y_test)
# Evaluate Model
knn_eval = evaluate_model(knn, encoded_test, y_test)

# Intitialize figure with two plots
#fig, (ax1, ax2) = plt.subplots(1, 2)
#fig.suptitle('Model Comparison', fontsize=16, fontweight='bold')
#fig.set_figheight(7)
#fig.set_figwidth(14)
#fig.set_facecolor('white')

# First plot
## set bar size
#barWidth = 0.2
#dtc_score = [dtc_eval['acc'], dtc_eval['prec'], dtc_eval['rec'], dtc_eval['f1'], dtc_eval['kappa']]
#rf_score = [rf_eval['acc'], rf_eval['prec'], rf_eval['rec'], rf_eval['f1'], rf_eval['kappa']]
#nb_score = [nb_eval['acc'], nb_eval['prec'], nb_eval['rec'], nb_eval['f1'], nb_eval['kappa']]
#knn_score = [knn_eval['acc'], knn_eval['prec'], knn_eval['rec'], knn_eval['f1'], knn_eval['kappa']]

## Set position of bar on X axis
#r1 = np.arange(len(dtc_score))
#r2 = [x + barWidth for x in r1]
#r3 = [x + barWidth for x in r2]
#r4 = [x + barWidth for x in r3]

## Make the plot
#ax1.bar(r1, dtc_score, width=barWidth, edgecolor='white', label='Decision Tree')
#ax1.bar(r2, rf_score, width=barWidth, edgecolor='white', label='Random Forest')
#ax1.bar(r3, nb_score, width=barWidth, edgecolor='white', label='Naive Bayes')
#ax1.bar(r4, knn_score, width=barWidth, edgecolor='white', label='K-Nearest Neighbors')

## Configure x and y axis
#ax1.set_xlabel('Metrics', fontweight='bold')
#labels = ['Accuracy', 'Precision', 'Recall', 'F1', 'Kappa']
#ax1.set_xticks([r + (barWidth * 1.5) for r in range(len(dtc_score))], )
#ax1.set_xticklabels(labels)
#ax1.set_ylabel('Score', fontweight='bold')
#ax1.set_ylim(0, 1)

## Create legend & title
#ax1.set_title('Evaluation Metrics', fontsize=14, fontweight='bold')
#ax1.legend()

# Second plot
## Comparing ROC Curve
#ax2.plot(dtc_eval['fpr'], dtc_eval['tpr'], label='Decision Tree, auc = {:0.5f}'.format(dtc_eval['auc']))
#ax2.plot(rf_eval['fpr'], rf_eval['tpr'], label='Random Forest, auc = {:0.5f}'.format(rf_eval['auc']))
#ax2.plot(nb_eval['fpr'], nb_eval['tpr'], label='Naive Bayes, auc = {:0.5f}'.format(nb_eval['auc']))
#ax2.plot(knn_eval['fpr'], knn_eval['tpr'], label='K-Nearest Nieghbor, auc = {:0.5f}'.format(knn_eval['auc']))

## Configure x and y axis
#ax2.set_xlabel('False Positive Rate', fontweight='bold')
#ax2.set_ylabel('True Positive Rate', fontweight='bold')

## Create legend & title
#ax2.set_title('ROC Curve', fontsize=14, fontweight='bold')
#ax2.legend(loc=4)
#plt.savefig("model_comparison.png")
#plt.show()

# Print result
print("####### Random Forest Classifier #######")
print('Accuracy:', rf_eval['acc'])
print('Precision:', rf_eval['prec'])
print('Recall:', rf_eval['rec'])
print('F1 Score:', rf_eval['f1'])
print('Cohens Kappa Score:', rf_eval['kappa'])
print('Area Under Curve:', rf_eval['auc'])
print('Confusion Matrix:\n', rf_eval['cm'])

# Print result
print('\n####### Decision Tree Classifier #######')
print('Accuracy:', dtc_eval['acc'])
print('Precision:', dtc_eval['prec'])
print('Recall:', dtc_eval['rec'])
print('F1 Score:', dtc_eval['f1'])
print('Cohens Kappa Score:', dtc_eval['kappa'])
print('Area Under Curve:', dtc_eval['auc'])
print('Confusion Matrix:\n', dtc_eval['cm'])

# Print result
print('\n####### K-Nearest Neighbours Classifier #######')
print('Accuracy:', knn_eval['acc'])
print('Precision:', knn_eval['prec'])
print('Recall:', knn_eval['rec'])
print('F1 Score:', knn_eval['f1'])
print('Cohens Kappa Score:', knn_eval['kappa'])
print('Area Under Curve:', knn_eval['auc'])
print('Confusion Matrix:\n', knn_eval['cm'])

# Print result
print('\n####### Naive Bayes Classifier #######')
print('Accuracy:', nb_eval['acc'])
print('Precision:', nb_eval['prec'])
print('Recall:', nb_eval['rec'])
print('F1 Score:', nb_eval['f1'])
print('Cohens Kappa Score:', nb_eval['kappa'])
print('Area Under Curve:', nb_eval['auc'])
print('Confusion Matrix:\n', nb_eval['cm'])
