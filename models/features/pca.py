import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def pca_reduction(input_csv, output_csv, n_components=100):
    # Load the data
    df = pd.read_csv(input_csv)

    # Separate ID and target column
    ids = df["ID"]
    target = df["飆股"]
    features = df.drop(columns=["ID", "飆股"])

    # Standardize the features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # Apply PCA
    pca = PCA(n_components=n_components)
    features_pca = pca.fit_transform(features_scaled)

    # Convert back to DataFrame
    columns = [f"PCA_{i+1}" for i in range(n_components)]
    df_pca = pd.DataFrame(features_pca, columns=columns)
    df_pca.insert(0, "ID", ids)
    df_pca.insert(1, "飆股", target)

    # Save the transformed data
    df_pca.to_csv(output_csv, index=False)
    print(f"PCA reduction completed! Saved to {output_csv}")

if __name__ == "__main__":
    csv_path = "ML_stock/data/cleaned_sample.csv"
    output_path = "ML_stock/data/sample_pca.csv"
    pca_reduction(csv_path, output_path)
