import os

folder_path = "training_data/order_data"

for filename in os.listdir(folder_path):
    if filename.startswith("._"):
        new_filename = filename[2:]
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
