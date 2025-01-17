import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Load the dataset
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx'
data = pd.read_excel(url)

# Inspect the general data structure
print(data.head())
print(data.info())

# Drop any rows with missing values
data.dropna(inplace=True)

# Extract the relevant features for clustering

data['TotalPrice'] = data['Quantity'] * data['UnitPrice']

# Aggregate data to create customer-level features
customer_data = data.groupby('CustomerID').agg({
    'InvoiceNo': 'nunique',       # Number of unique purchases
    'Quantity': 'sum',            # Total quantity purchased
    'TotalPrice': 'sum'           # Total spending
}).rename(columns={'InvoiceNo': 'NumPurchases', 'Quantity': 'TotalQuantity'})

print(customer_data.head())

# Standardize the features
scaler = StandardScaler()
customer_data_scaled = scaler.fit_transform(customer_data)

print(customer_data_scaled[:5])

# Determine the optimal number of clusters using the Elbow method
inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(customer_data_scaled)
    inertia.append(kmeans.inertia_)

# Plotting the Elbow curve
plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), inertia, marker='o', linestyle='--')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.show()

# Based on the elbow curve, choose the optimal number of clusters (e.g., k=3)
optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
customer_data['Cluster'] = kmeans.fit_predict(customer_data_scaled)

print(customer_data.head())

# Code below is aimed at analyzing the clusters
cluster_analysis = customer_data.groupby('Cluster').mean()
print(cluster_analysis)

# The following is used to visualize the clusters
plt.figure(figsize=(10, 8))
sns.scatterplot(x=customer_data['TotalQuantity'], y=customer_data['TotalPrice'], hue=customer_data['Cluster'], palette='viridis')
plt.xlabel('Total Quantity Purchased')
plt.ylabel('Total Spending')
plt.title('Customer Segmentation')
plt.show()


