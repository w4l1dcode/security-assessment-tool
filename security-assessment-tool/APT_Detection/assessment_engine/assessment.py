import pandas as pd
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
import APT_Detection.assessment_engine.data_preprocessor as data_preprocessor
import APT_Detection.assessment_engine.sniff_network as sniff_network


def sniff(interface="en0"):
    sniff_network.execute_cicflowmeter(interface)


def predict():
    # Load the model
    model = load_model('APT_Detection/AI_model/models/model.h5')

    # Load the data to predict
    data_to_predict = pd.read_csv('APT_Detection/assessment_engine/assessment_data.csv')

    # Store the IP addresses in separate variables
    src_ips = data_to_predict['src_ip']
    dst_ips = data_to_predict['dst_ip']
    src_prts = data_to_predict['Src Port']
    dst_prts = data_to_predict['Dst Port']

    # Drop the IP address column from the data
    data_to_predict = data_to_predict.drop(['src_ip', 'dst_ip'], axis=1)
    from joblib import dump, load
    # Load the scaler and transform the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data_to_predict)

    # Make predictions
    pred = model.predict(scaled_data)

    return pred, src_ips, dst_ips, src_prts, dst_prts

def calculate_apt_traffic(flowlist, pred):
    # Calculate the percentage of APT_Detection traffic
    pct_apt = len(flowlist) / len(pred) * 100

    # Display the percentage of APT_Detection traffic to the user
    # print(f"Percentage of APT traffic: {pct_apt:.2f}%")

    return pct_apt


def get_apt_flow(pred, src_ips, dst_ips, src_prts, dst_prts):
    # Print the predicted values for the positive Report
    flowlist=[]
    for i in range(len(pred)):
        if np.any(pred[i] == 1):
            flowlist.append([src_ips[i], dst_ips[i], int(src_prts[i]), int(dst_prts[i])])

            # print(f"Positive result for {src_ips[i]} -> {dst_ips[i]}")
    # print("Length of flowlist:", len(flowlist))
    return flowlist


def predict_apt_file(file):
    data_preprocessor.normalize_data(file)
    # Get predicted values
    pred, src_ips, dst_ips, src_prts, dst_prts = predict()

    # Get all the source -> destination IP addresses of flows that are recognized as APT_Detection traffic
    flowlist = get_apt_flow(pred, src_ips, dst_ips, src_prts, dst_prts)

    # Calculate the percentage of APT_Detection traffic
    percentage = calculate_apt_traffic(flowlist, pred)

    return percentage, flowlist


def predict_apt(interface="en0"):
    # Sniff all TCP packets in the network
    sniff(interface)

    # Preprocess the data accordingly for the AI model
    data_preprocessor.normalize_data()

    # Get predicted values
    pred, src_ips, dst_ips, src_ports, dst_ports = predict()

    # Get all the source -> destination IP addresses of flows that are recognized as APT_Detection traffic
    flowlist = get_apt_flow(pred, src_ips, dst_ips, src_ports, dst_ports)

    # Calculate the percentage of APT_Detection traffic
    percentage = calculate_apt_traffic(flowlist, pred)

    return percentage, flowlist