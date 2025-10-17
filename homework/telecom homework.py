"""
Homework: K-Means Clustering & PCA on Telecom Data
Dataset: Telco Customer Churn (Kaggle)
Goal: Discover customer segments using unsupervised learning
"""

# --- Import libraries ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# -----------------------------
# Part A: Load and preprocess data
# -----------------------------
print("📥 Loading dataset...")

url = "https://raw.githubusercontent.com/ybifoundation/Dataset/main/Telco%20Customer%20Churn.csv"
df = pd.read_csv(url)

print(f"Data loaded successfully with shape: {df.shape}")
print("\nPreview of dataset:")
print(df.head())

# Drop the customer ID (not useful for clustering)
df.drop('customerID', axis=1, inplace=True)

# Convert TotalCharges to numeric (some entries are blank)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)

# Encode categorical variables (convert Yes/No etc. to 1/0)
df_encoded = pd.get_dummies(df, drop_first=True)

# Standardize numeric values to have mean 0 and variance 1
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_encoded)

print("\n✅ Data preprocessing complete!")

# -----------------------------
# Part B: PCA – Dimensionality Reduction
# -----------------------------
print("\n🔍 Applying PCA to reduce data to 2 dimensions...")

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

explained_var = np.sum(pca.explained_variance_ratio_)
print(f"Total variance explained by 2 components: {explained_var:.2%}")

# Visualize PCA results
plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], s=10, alpha=0.5)
plt.title('PCA: 2D Projection of Telecom Customers')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()

# -----------------------------
# Part C: K-Means Clustering
# -----------------------------
print("\n🤖 Running K-Means clustering on PCA data...")

inertias = []
silhouettes = []
K_range = range(2, 10)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_pca)
    inertias.append(kmeans.inertia_)
    silhouettes.append(silhouette_score(X_pca, kmeans.labels_))

# Plot Elbow and Silhouette curves
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].plot(K_range, inertias, marker='o')
ax[0].set_title('Elbow Method')
ax[0].set_xlabel('Number of Clusters (K)')
ax[0].set_ylabel('Inertia')

ax[1].plot(K_range, silhouettes, marker='o', color='green')
ax[1].set_title('Silhouette Score')
ax[1].set_xlabel('Number of Clusters (K)')
ax[1].set_ylabel('Score')
plt.show()

# Choose K with best Silhouette score
best_k = K_range[np.argmax(silhouettes)]
print(f"\n🎯 Best number of clusters (K) based on Silhouette score: {best_k}")

# Fit final model
kmeans_final = KMeans(n_clusters=best_k, random_state=42)
df['Cluster'] = kmeans_final.fit_predict(X_pca)

# Visualize clusters in PCA space
plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['Cluster'], cmap='viridis', s=10)
plt.title(f'K-Means Clusters (K={best_k}) in PCA Space')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()

# -----------------------------
# Part D: Interpret and Analyze Clusters
# -----------------------------
print("\n📊 Analyzing clusters for business insights...")

# Aggregate useful metrics per cluster
cluster_summary = df.groupby('Cluster')[['MonthlyCharges', 'tenure', 'TotalCharges']].mean()
cluster_summary['ChurnRate (%)'] = df.groupby('Cluster')['Churn_Yes'].mean() * 100

print("\nCluster Summary:")
print(cluster_summary.round(2))

print("\n🧠 Insights:")
print("- Clusters may represent different customer profiles, such as:")
print("  • High-paying long-term customers with low churn risk.")
print("  • Short-tenure customers with high churn tendency.")
print("  • Moderate users with average billing and loyalty.")
print("\n✅ Task complete: PCA, clustering, and insights generated.")
