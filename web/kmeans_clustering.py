import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import silhouette_score, calinski_harabasz_score
import streamlit as sl


class KMeansClustering:
    def __init__(self):
        pass

    def fill_missing_values(self, df):
        df_filled = df.fillna(df.mean())
        return df_filled

    def remove_duplicates(self, data):
        df_without_duplicates = data.drop_duplicates()
        return df_without_duplicates

    def encode_categorical_data(self, data):
        for column in data.columns[:]:
            if data[column].dtype == "object":
                data[column] = pd.Categorical(data[column]).codes
        return data

    def remove_outliers_iqr(self, df, iqr_factor=1.5):
        conditions = []
        for col in df.columns[:]:
            lower_bound = df[col].quantile(5 / 100)
            upper_bound = df[col].quantile(95 / 100)
            condition = (df[col] < lower_bound) | (df[col] > upper_bound)
            conditions.append(condition)

        combined_condition = ~pd.concat(conditions, axis=1).any(axis=1)
        return df[combined_condition]

    def perform_pca(self, data):
        if len(data.columns) > 10:
            pca = PCA(n_components=10)
            pca.fit(data)
            return pd.DataFrame(pca.transform(data))

    def data_preprocess_for_the_clustering_algorithms(self, data):
        data = self.fill_missing_values(data)
        data = self.remove_duplicates(data)
        data = self.encode_categorical_data(data)
        data = self.remove_outliers_iqr(data)
        data = self.perform_pca(data)
        return data

    def kmeans_algorithm(self, data_frame):
        X = self.data_preprocess_for_the_clustering_algorithms(data_frame.iloc[:, :-1])
        n_clusters = sl.number_input(
            'Specify the number of clusters "k" for the k-means clustering algorithm: '
        )
        n_clusters = int(n_clusters)
        if n_clusters <= len(X) and n_clusters > 1:
            kmeans = KMeans(n_clusters=n_clusters)
            kmeans.fit(X)
            labels = kmeans.labels_
            inertia = kmeans.inertia_
            silhouette = round((silhouette_score(X, labels) * 100), 3)
            sl.write(f"Silhouette Score: {silhouette}")
        else:
            sl.error(
                "The number of clusters must be more than 1 and cannot exceed the number of instances. Please try again"
            )
