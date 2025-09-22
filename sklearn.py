# Import necessary libraries
import numpy as np  # for numerical operations
import matplotlib.pyplot as plt  # for plotting
import pandas as pd  # for handling data in DataFrame format
import seaborn as sns  # for better visualization

# Load the dataset from a CSV file
df = pd.read_csv(r'C:\Users\aashutosh\Downloads\Data (2).csv')  # replace with your file path

# Separate the features (all columns except the last one) and target (last column)
x = df.iloc[:, :-1].values  # Features: all columns except the last one
y = df.iloc[:, -1].values  # Target: the last column

# Handle missing data: Fill missing values with the mean of the column
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy="mean")  # Instantiate the imputer to fill missing values with the column mean
x[:, 1:3] = imputer.fit_transform(x[:, 1:3])  # Apply imputer to columns 1 and 2 (indexing starts from 0)

# Encode categorical data: Convert string labels into numeric labels
from sklearn.preprocessing import LabelEncoder
labelencoder_x = LabelEncoder()  # Instantiate the label encoder
x[:, 0] = labelencoder_x.fit_transform(x[:, 0])  # Encode the categorical values in the first column (index 0)

# Split the dataset into training and testing sets (70% train, 30% test)
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)  # 70-30 split






