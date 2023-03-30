# collect data and extract features and finally predict
from joblib import load
import pandas as pd
from numpy import max
import Phishing_Detection.assessment_engine.email_connection as email_connection
import Phishing_Detection.assessment_engine.feature_extraction as feature_extraction
from sklearn import preprocessing


def predict_phishing_file(filename):
    print("Starting feature extraction...")
    feature_extraction.extract_features(filename)
    print("Finished extracting features from all urls!")
    to_predict_urls = pd.read_csv("Phishing_detection/assessment_engine/to_predict.csv", header=0)
    X = to_predict_urls.drop('url', axis=1).values
    X = preprocessing.scale(X)    # Load pretrained model
    print("Loading AI model for prediction")
    mlp = load("Phishing_Detection/AI_model/tuned_phishing_model.joblib")
    prediction = mlp.predict(X)
    probability = max(mlp.predict_proba(X), axis=1) * 100
    to_predict_urls["result"] = prediction
    to_predict_urls["probability"] = probability
    dataframe = pd.read_csv(filename, header=0)
    dataframe = pd.merge(dataframe, to_predict_urls[["url", "result", "probability"]], on="url", how='left')
    dataframe.fillna(value={"result": 0}, inplace=True)
    mapping = {-1: "phishing", 0: "unavailable", 1: "benign"}
    dataframe.replace({"result": mapping}, inplace=True)
    dataframe.to_csv('Phishing_detection/assessment_engine/predicted_result.csv', index=False)
    print("Prediction completed, click \"show  result\" to see dashboard.")


def predict_phishing(username='lars.de.loenen@gmail.com', password='diiwazblxakjnads', mailbox='[Gmail]/Spam'):
    # Collect urls
    # Goes through the mailbox specified and scrapes mail-id, sender, subject and first found url
    print("Collecting urls from: " + mailbox)
    email_connection.collect_emails_and_scrape_urls(username, password, mailbox)
    dataframe = pd.read_csv("Phishing_detection/assessment_engine/scrape_urls.csv",
                            names=['email-id', 'sender', 'subject', 'url'])
    print("Starting feature extraction...")
    feature_extraction.extract_features()
    print("Finished extracting features from all urls!")
    to_predict_urls = pd.read_csv("Phishing_detection/assessment_engine/to_predict.csv", header=0)
    X = to_predict_urls.drop('url', axis=1).values
    X = preprocessing.scale(X)
    # Load pretrained model
    print("Loading AI model for prediction")
    mlp = load("Phishing_Detection/AI_model/tuned_phishing_model.joblib")
    prediction = mlp.predict(X)
    probability = max(mlp.predict_proba(X), axis=1) * 100
    to_predict_urls["result"] = prediction
    to_predict_urls["probability"] = probability
    dataframe = pd.merge(dataframe, to_predict_urls[["url", "result", "probability"]], on="url", how='left')
    dataframe.fillna(value={"result": 0}, inplace=True)
    mapping = {-1: "phishing", 0: "unavailable", 1: "benign"}
    dataframe.replace({"result": mapping}, inplace=True)
    dataframe.to_csv('Phishing_detection/assessment_engine/predicted_result.csv', index=False)
    print("Prediction completed, click \"show  result\" to see dashboard.")
    return dataframe

# if __name__ == '__main__':
#     predict_phishing()
#     dataframe = pd.read_csv("scrape_urls.csv", names=['email-id', 'sender', 'subject', 'url'])
#     feature_extraction.extract_features()
#
#     to_predict_urls = pd.read_csv("to_predict.csv",header=0)
#     print(to_predict_urls)
#     X = to_predict_urls.drop('url', axis=1).values
#
#     mlp = load("../AI_model/tuned_phishing_model.joblib")
#
#     prediction = mlp.predict(X)
#     predicted_proba = mlp.predict_proba(X)
#     to_predict_urls["result"] = prediction
#     dataframe.reset_index()
#     to_predict_urls.reset_index()
#
#     dataframe = pd.merge(dataframe, to_predict_urls[["url","result"]], on="url", how='left')
#     dataframe.fillna(value={"result":0}, inplace=True)
#     dataframe.to_csv('predicted_result.csv', index=False)
#     print(to_predict_urls.head())
#     print(prediction)
#     print(predicted_proba)
