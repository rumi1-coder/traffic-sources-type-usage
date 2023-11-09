#import pandas as pd

# path of the file to read
#file_path = "training_data\order_data\order_data_2016-01-01"

# read the file into a DataFrame
#df = pd.read_csv(file_path, delimiter="\t", header=None, names=["order_id", "driver_id", "passenger_id", "start_district_hash", "dest_district_hash", "price", "date"])

# print the column names and data types
#print(df.dtypes)
import os
import pandas as pd

# Define the directory where the files are located
directory = 'training_data\order_data'

# Create an empty list to store the DataFrames
dfs = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.startswith("order_data_") :
        # Read the file into a DataFrame
        df = pd.read_csv(os.path.join(directory, filename), delimiter='\t', header=None)
        #print(df)
        # Add the DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames in the list into a single DataFrame

order_data = pd.concat(dfs, ignore_index=True)

# Print the column names and data types
#print(order_data.columns)
#print(order_data.dtypes)
