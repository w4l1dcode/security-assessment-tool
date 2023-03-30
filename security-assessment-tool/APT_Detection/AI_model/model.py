# Import the necessary libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from keras.layers import Input, Dense
from keras.models import Model
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

# Load the data from the CSV file
data = pd.read_csv('../data_collection/trainings_data.csv')

# Split the data into features and labels
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Scale the data
sc = StandardScaler()
X = sc.fit_transform(X)

# Split the data into training, testing and validation sets
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
history = autoencoder.fit(X_train, X_train, epochs=10, batch_size=10,
                          shuffle=False, validation_data=(X_val, X_val))


# Create the encoding model
encoder = Model(input_layer, encoded)

# Encode the data
encoded_train = encoder.predict(X_train)
encoded_test = encoder.predict(X_test)

# Train a classifier on the encoded data
classifier = RandomForestClassifier(random_state=0)
classifier.fit(encoded_train, y_train)

# save the model
autoencoder.save("models/model.h5")


def plot_loss():
    # Extract the loss values from the history object
    train_loss = history.history['loss']
    val_loss = history.history['val_loss']

    # Plot the loss function graph
    plt.plot(train_loss, label='Train Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig("loss_graph.png")
    plt.show()


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


def plot_confusion_matrix(cm):
    # Plot the confusion matrix as a bar graph
    fig, ax = plt.subplots()
    im = ax.imshow(cm, cmap='Blues')

    # Add labels to the plot
    ax.set_xticks(np.arange(2))
    ax.set_yticks(np.arange(2))
    ax.set_xticklabels(['Predicted Normal', 'Predicted APT_Detection'])
    ax.set_yticklabels(['Actual Normal', 'Actual APT_Detection'])

    # Add annotations to the cells
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center", color="black")

    # Display the plot
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.savefig("confusion_matrix.png")
    plt.show()


def plot_roc(fpr, tpr, roc_auc):
    plt.figure()
    plt.plot(fpr, tpr, color='red', label='AUC = %0.2f)' % roc_auc)
    plt.xlim((0, 1))
    plt.ylim((0, 1))
    plt.plot([0, 1], [0, 1], color="navy", linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Autoencoder')
    plt.legend(loc='lower right')
    plt.savefig("ROC-curve.png")
    plt.show()


#class_eval = evaluate_model(classifier, encoded_test, y_test)