import pandas as pd


def merge_data():
    # Load the datasets into pandas dataframes
    df1_public = pd.read_csv("raw_data_files/enp0s3-monday.pcap_Flow.csv")
    df1_private = pd.read_csv("raw_data_files/enp0s3-monday-pvt.pcap_Flow.csv")
    df2_public = pd.read_csv("raw_data_files/enp0s3-public-tuesday.pcap_Flow.csv")
    df2_private = pd.read_csv("raw_data_files/enp0s3-pvt-tuesday.pcap_Flow.csv")
    df3_public = pd.read_csv("raw_data_files/enp0s3-public-wednesday.pcap_Flow.csv")
    df3_private = pd.read_csv("raw_data_files/enp0s3-pvt-wednesday.pcap_Flow.csv")
    df4_public = pd.read_csv("raw_data_files/enp0s3-public-thursday.pcap_Flow.csv")
    df4_private = pd.read_csv("raw_data_files/enp0s3-pvt-thursday.pcap_Flow.csv")
    df5_public = pd.read_csv("raw_data_files/enp0s3-tcpdump-friday.pcap_Flow.csv")
    df5_private = pd.read_csv("raw_data_files/enp0s3-tcpdump-pvt-friday.pcap_Flow.csv")

    # Label the datasets as per APT_Detection or Normal traffic (APT_Detection = 1, NORMAL = 0)
    df1_public["Label"] = 0
    df1_private["Label"] = 0
    df2_public["Label"] = 1
    df2_private["Label"] = 0
    df3_public["Label"] = 1
    df3_private["Label"] = 1
    df4_public["Label"] = 1
    df4_private["Label"] = 1
    df5_public["Label"] = 1
    df5_private["Label"] = 1

    # Merge the datasets into one file
    merged_df = pd.concat([df1_public, df1_private, df2_public, df2_private,
                           df3_public, df3_private, df4_public, df4_private,
                           df5_public, df5_private], axis=0)

    # Remove the columns we don't need
    merged_df = merged_df.drop(["Activity", "Stage"], axis=1)

    # Save the merged dataset to a csv file
    merged_df.to_csv("trainings_data.csv", index=False)


def normalize_data():
    # Load the data into a pandas dataframe
    df = pd.read_csv("trainings_data.csv")

    # Remove all object columns
    df_numeric = df.select_dtypes(exclude=['object'])

    df_numeric.to_csv("trainings_data.csv", index=False)



if __name__ == "__main__":
    merge_data()
    normalize_data()
