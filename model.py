import math
import os
import pandas as pd

# Define a function to split the data into training and testing sets
def train_test_split(data, test_ratio=0.3):
    train_size = int(len(data) * (1 - test_ratio))
    train_data = data[:train_size]
    test_data = data[train_size:]
    return train_data, test_data

# Define a function to calculate entropy
def entropy(labels):
    counts = {}
    for label in labels:
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    ent = 0
    for count in counts.values():
        p = count / len(labels)
        ent -= p * math.log(p, 2)
    return ent

# Define a function to calculate information gain
def info_gain(data, feature, target):
    ent = entropy(data[target])
    values = set(data[feature])
    for value in values:
        subset = data[data[feature] == value]
        ent -= len(subset) / len(data) * entropy(subset[target])
    return ent

# Define a function to recursively build a decision tree
def build_tree(data, features, target):
    if len(set(data[target])) == 1:
        return data[target].iloc[0]
    if len(features) == 0:
        return data[target].value_counts().idxmax()
    best_feature = max(features, key=lambda feature: info_gain(data, feature, target))
    tree = {best_feature: {}}
    for value in set(data[best_feature]):
        subset = data[data[best_feature] == value]
        if len(subset) == 0:
            tree[best_feature][value] = data[target].value_counts().idxmax()
        else:
            subtree = build_tree(subset, [f for f in features if f != best_feature], target)
            tree[best_feature][value] = subtree
    return tree

# Define a function to make predictions using a decision tree
def predict(tree, data):
    if isinstance(tree, str):
        return tree
    feature, subtree_dict = next(iter(tree.items()))
    subtree = subtree_dict.get(data[feature], None)
    if subtree is None:
        return data[feature].value_counts().idxmax()
    return predict(subtree, data)

# Load the preprocessed data
folder_path = 'preprocessed_data'
data_path = os.path.join(folder_path, 'data.csv')
data = pd.read_csv(data_path)

# Define the target variable and the features to use for prediction
target = 'demand'
features = ['weekday', 'hour', 'region', 'poi', 'weather']

# Split the data into training and testing sets
train_data, test_data = train_test_split(data)

# Build the decision tree
tree = build_tree(train_data, features, target)

# Make predictions on the test data
predictions = []
for i in range(len(test_data)):
    row = test_data.iloc[i]
    prediction = predict(tree, row)
    predictions.append(prediction)

# Calculate accuracy
correct_count = sum(predictions[i] == test_data[target].iloc[i] for i in range(len(test_data)))
accuracy = correct_count / len(test_data)
print(f'Accuracy: {accuracy}')
