import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Define the path to the training data folder
folder_path = 'training_data'

# Load the cluster map file
cluster_map_path = os.path.join(folder_path, 'cluster_map', 'cluster_map')
with open(cluster_map_path, 'r') as f:
    cluster_map = dict(line.strip().split('\t') for line in f.readlines())

# Load the order data file
order_data_path = os.path.join(folder_path, 'order_data')
order_data = pd.read_csv(order_data_path, header=None, names=['order_id', 'driver_id', 'passenger_id', 'start_region_hash', 'dest_region_hash', 'price', 'time'])

# Load the POI data file
poi_data_path = os.path.join(folder_path, 'poi_data')
poi_data = pd.read_csv(poi_data_path, header=None, names=['region_hash', 'poi_class', 'poi_class_count'])

# Load the weather data file
weather_data_path = os.path.join(folder_path, 'weather_data')
weather_data = pd.read_csv(weather_data_path, header=None, names=['Time', 'Weather', 'temperature',])

# Load the traffic data files
traffic_data_folder_path = os.path.join(folder_path, 'traffic_data')
traffic_data = pd.DataFrame()
for filename in os.listdir(traffic_data_folder_path):
    if filename.endswith('.csv'):
        filepath = os.path.join(traffic_data_folder_path, filename)
        region_hash = filename.split('.')[0]
        df = pd.read_csv(filepath, header=None, names=['time', 'traffic_flow'])
        df['region_hash'] = region_hash
        traffic_data = pd.concat([traffic_data, df])

# Merge order data with traffic data and POI data
data = pd.merge(order_data, traffic_data, on=['time', 'start_region_hash'], how='left')
data = pd.merge(data, poi_data, on=['region_hash'], how='left')

# Drop unnecessary columns
data.drop(['order_id', 'driver_id', 'passenger_id', 'start_region_hash', 'dest_region_hash', 'region_hash', 'time'], axis=1, inplace=True)

# Encode categorical variables
le = LabelEncoder()
data['start_region'] = le.fit_transform(data['start_region'].map(cluster_map))
data['dest_region'] = le.fit_transform(data['dest_region'].map(cluster_map))
data['poi_class'] = le.fit_transform(data['poi_class'])
data['region'] = le.fit_transform(data['region_hash'].map(cluster_map))
data['Weather'] = le.fit_transform(data['Weather'])

# Fill missing values with 0
data.fillna(0, inplace=True)

# Write preprocessed data to file
data.to_csv('data.csv', index=False)
