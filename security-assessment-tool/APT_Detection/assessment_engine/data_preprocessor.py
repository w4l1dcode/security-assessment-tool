import pandas as pd

# read in the csv file to a Pandas DataFrame
# df = pd.read_csv('APT_Detection/assessment_engine/flows.csv')


def normalize_data(directory='APT_Detection/assessment_engine/flows.csv'):
    df = pd.read_csv(directory)
    # rename columns
    df_refactored = df.rename(columns={
        'Src IP': 'src_ip',
        'Dst IP': 'dst_ip',
        'src_port': 'Src Port',
        'dst_port': 'Dst Port',
        'protocol': 'Protocol',
        'flow_duration': 'Flow Duration',
        'tot_fwd_pkts': 'Total Fwd Packet',
        'tot_bwd_pkts': 'Total Bwd packets',
        'totlen_fwd_pkts': 'Total Length of Fwd Packet',
        'totlen_bwd_pkts': 'Total Length of Bwd Packet',
        'fwd_pkt_len_max': 'Fwd Packet Length Max',
        'fwd_pkt_len_min': 'Fwd Packet Length Min',
        'fwd_pkt_len_mean': 'Fwd Packet Length Mean',
        'fwd_pkt_len_std': 'Fwd Packet Length Std',
        'bwd_pkt_len_max': 'Bwd Packet Length Max',
        'bwd_pkt_len_min': 'Bwd Packet Length Min',
        'bwd_pkt_len_mean': 'Bwd Packet Length Mean',
        'bwd_pkt_len_std': 'Bwd Packet Length Std',
        'flow_byts_s': 'Flow Bytes/s',
        'flow_pkts_s': 'Flow Packets/s',
        'fwd_pkts_s': 'Fwd Packets/s',
        'bwd_pkts_s': 'Bwd Packets/s',
        'flow_iat_mean': 'Flow IAT Mean',
        'flow_iat_std': 'Flow IAT Std',
        'flow_iat_max': 'Flow IAT Max',
        'flow_iat_min': 'Flow IAT Min',
        'fwd_iat_tot': 'Fwd IAT Total',
        'fwd_iat_mean': 'Fwd IAT Mean',
        'fwd_iat_std': 'Fwd IAT Std',
        'fwd_iat_max': 'Fwd IAT Max',
        'fwd_iat_min': 'Fwd IAT Min',
        'bwd_iat_tot': 'Bwd IAT Total',
        'bwd_iat_mean': 'Bwd IAT Mean',
        'bwd_iat_std': 'Bwd IAT Std',
        'bwd_iat_max': 'Bwd IAT Max',
        'bwd_iat_min': 'Bwd IAT Min',
        'fwd_psh_flags': 'Fwd PSH Flags',
        'bwd_psh_flags': 'Bwd PSH Flags',
        'fwd_urg_flags': 'Fwd URG Flags',
        'bwd_urg_flags': 'Bwd URG Flags',
        'fwd_header_len': 'Fwd Header Length',
        'bwd_header_len': 'Bwd Header Length',
        'pkt_len_min': 'Packet Length Min',
        'pkt_len_max': 'Packet Length Max',
        'pkt_len_mean': 'Packet Length Mean',
        'pkt_len_std': 'Packet Length Std',
        'pkt_len_var': 'Packet Length Variance',
        'fin_flag_cnt': 'FIN Flag Count',
        'syn_flag_cnt': 'SYN Flag Count',
        'rst_flag_cnt': 'RST Flag Count',
        'psh_flag_cnt': 'PSH Flag Count',
        'ack_flag_cnt': 'ACK Flag Count',
        'urg_flag_cnt': 'URG Flag Count',
        'cwe_flag_count': 'CWR Flag Count',
        'ece_flag_cnt': 'ECE Flag Count',
        'down_up_ratio': 'Down/Up Ratio',
        'pkt_size_avg': 'Average Packet Size',
        'init_fwd_win_byts': 'FWD Init Win Bytes',
        'init_bwd_win_byts': 'Bwd Init Win Bytes',
        'active_max': 'Active Max',
        'active_min': 'Active Min',
        'active_mean': 'Active Mean',
        'active_std': 'Active Std',
        'idle_max': 'Idle Max',
        'idle_min': 'Idle Min',
        'idle_mean': 'Idle Mean',
        'idle_std': 'Idle Std',
        'fwd_byts_b_avg': 'Fwd Bytes/Bulk Avg',
        'fwd_pkts_b_avg': 'Fwd Packet/Bulk Avg',
        'bwd_byts_b_avg': 'Bwd Bytes/Bulk Avg',
        'bwd_pkts_b_avg': 'Bwd Packet/Bulk Avg',
        'fwd_blk_rate_avg': 'Fwd Bulk Rate Avg',
        'bwd_blk_rate_avg': 'Bwd Bulk Rate Avg',
        'fwd_seg_size_avg': 'Fwd Segment Size Avg',
        'fwd_seg_size_min': 'Fwd Seg Size Min',
        'fwd_act_data_pkts': 'Fwd Act Data Pkts',
        'bwd_seg_size_avg': 'Bwd Segment Size Avg',
        'subflow_fwd_pkts': 'Subflow Fwd Packets',
        'subflow_bwd_pkts': 'Subflow Bwd Packets',
        'subflow_fwd_byts': 'Subflow Fwd Bytes',
        'subflow_bwd_byts': 'Subflow Bwd Bytes'
    })

    # Select object columns and keep only those that are 'src_ip' and 'dst_ip'
    df_object = df_refactored.select_dtypes(include='object')
    df_object = df_object[['src_ip', 'dst_ip']]

    # Select all columns except object columns
    df_float = df_refactored.select_dtypes(exclude='object')

    # Convert all selected columns to float type
    df_float = df_float.astype('float')

    # Combine the two dataframes to create the final output
    df_combined = pd.concat([df_object, df_float], axis=1)

    # Define the desired column order
    new_order = ["src_ip", "dst_ip", "Src Port", "Dst Port", "Protocol", "Flow Duration", "Total Fwd Packet",
                 "Total Bwd packets", "Total Length of Fwd Packet", "Total Length of Bwd Packet",
                 "Fwd Packet Length Max", "Fwd Packet Length Min", "Fwd Packet Length Mean", "Fwd Packet Length Std",
                 "Bwd Packet Length Max", "Bwd Packet Length Min", "Bwd Packet Length Mean", "Bwd Packet Length Std", "Flow Bytes/s",
                 "Flow Packets/s", "Flow IAT Mean", "Flow IAT Std", "Flow IAT Max", "Flow IAT Min",
                 "Fwd IAT Total", "Fwd IAT Mean", "Fwd IAT Std", "Fwd IAT Max", "Fwd IAT Min", "Bwd IAT Total", "Bwd IAT Mean",
                 "Bwd IAT Std", "Bwd IAT Max", "Bwd IAT Min", "Fwd PSH Flags", "Bwd PSH Flags", "Fwd URG Flags",
                 "Bwd URG Flags", "Fwd Header Length", "Bwd Header Length", "Fwd Packets/s", "Bwd Packets/s",
                 "Packet Length Min", "Packet Length Max", "Packet Length Mean", "Packet Length Std",
                 "Packet Length Variance", "FIN Flag Count", "SYN Flag Count", "RST Flag Count", "PSH Flag Count",
                 "ACK Flag Count", "URG Flag Count", "CWR Flag Count", "ECE Flag Count", "Down/Up Ratio",
                 "Average Packet Size", "Fwd Segment Size Avg", "Bwd Segment Size Avg", "Fwd Bytes/Bulk Avg",
                 "Fwd Packet/Bulk Avg", "Fwd Bulk Rate Avg", "Bwd Bytes/Bulk Avg", "Bwd Packet/Bulk Avg",
                 "Bwd Bulk Rate Avg", "Subflow Fwd Packets", "Subflow Fwd Bytes", "Subflow Bwd Packets",
                 "Subflow Bwd Bytes", "FWD Init Win Bytes", "Bwd Init Win Bytes", "Fwd Act Data Pkts",
                 "Fwd Seg Size Min", "Active Mean", "Active Std", "Active Max", "Active Min", "Idle Mean",
                 "Idle Std", "Idle Max", "Idle Min"]

    # Reorder the columns based on the new order
    df_reordered = df_combined[new_order]

    # Save the reordered dataframe to a new CSV file
    df_reordered.to_csv("APT_Detection/assessment_engine/assessment_data.csv", index=False)

normalize_data()