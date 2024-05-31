import pandas as pd
from sklearn.decomposition import PCA
from scipy.spatial.distance import pdist
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import silhouette_score
import streamlit as sl


class HierachicalClustering:
    def __init__(self):
        pass

    # Function that fills the missing values with the mean of the variables
    def fill_missing_values(self, df):
        df_filled = df.fillna(df.mean())
        return df_filled

    # Function that removes the duplicate instances
    def remove_duplicates(self, data):
        df_without_duplicates = data.drop_duplicates()
        return df_without_duplicates

    # Function that encodes categorical data into numerical
    def encode_categorical_data(self, data):
        for column in data.columns[:]:
            if data[column].dtype == "object":
                data[column] = pd.Categorical(data[column]).codes
        return data

    # Function that removes the outliers
    def remove_outliers_iqr(self, df, iqr_factor=1.5):
        conditions = []
        for col in df.columns[:]:
            lower_bound = df[col].quantile(5 / 100)
            upper_bound = df[col].quantile(95 / 100)
            condition = (df[col] < lower_bound) | (df[col] > upper_bound)
            conditions.append(condition)

        combined_condition = ~pd.concat(conditions, axis=1).any(axis=1)
        return df[combined_condition]

    # Function that performs dimensionality reduction using the PCA algorithm
    def perform_pca(self, data):
        if len(data.columns) > 10:
            pca = PCA(n_components=10)
            pca.fit(data)
            return pd.DataFrame(pca.transform(data))

    # Function for the preprocess of the data
    def data_preprocess_for_the_clustering_algorithms(self, data):
        data = self.fill_missing_values(data)
        data = self.remove_duplicates(data)
        data = self.encode_categorical_data(data)
        data = self.remove_outliers_iqr(data)
        data = self.perform_pca(data)
        return data

    # Function that implements the Hierarchical clustering algorithm
    def hierarchical_clustering(self, data, linkage="ward"):
        data = self.data_preprocess_for_the_clustering_algorithms(data.iloc[:, :-1])
        metrics = {
            "Euclidean": "euclidean",
            "City block": "cityblock",
            "Minkowski": "minkowski",
            "Chebyshev": "chebyshev",
        }

        metric_choice = sl.selectbox(
            "Please select the metric you would like to use:", metrics
        )

        metric = metrics[str(metric_choice)]

        distance_matrix = pdist(data, metric=metric)
        cluster_result = hierarchy.linkage(distance_matrix, method=linkage)
        cluster_labels = fcluster(cluster_result, 2, criterion="maxclust")
        silhouette = round(
            (silhouette_score(data, cluster_labels, metric=metric) * 100), 3
        )
        sl.write(f"Silhouette Score: {silhouette}")

        return silhouette
