import os
import pandas as pd

# Define the path to the training data folder
folder_path = 'training_data'

# Load the cluster map file
cluster_map_path = os.path.join(folder_path, 'cluster_map', 'cluster_map')
with open(cluster_map_path, 'r') as f:
    cluster_map = dict(line.strip().split('\t') for line in f.readlines())

# Load the order data file
order_data_path = os.path.join(folder_path, 'order_data')
print(order_data_path)
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

# Merge the order data with the cluster map to add region names
order_data['start_region'] = order_data['start_region_hash'].map(cluster_map)
order_data['dest_region'] = order_data['dest_region_hash'].map(cluster_map)

# Merge the POI data with the cluster map to add region names
poi_data['region'] = poi_data['region_hash'].map(cluster_map)

# Print some sample data
print('Order data:')
print(order_data.head())
print('POI data:')
print(poi_data.head())
print('Weather data:')
print(weather_data.head())
print('Traffic data:')
print(traffic_data.head())
