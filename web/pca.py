import streamlit as sl
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt


class PCADecomposition:
    def __init__(self, data_frame, n_components):
        self.data_frame = data_frame
        self.n_components = n_components
        self.pca = None

    def perform_pca(self):
        self.pca = PCA(n_components=self.n_components)
        self.pca.fit(self.data_frame)
        return self.pca

    def visualize_pca_scree(self):
        self.perform_pca()
        explained_variance = self.pca.explained_variance_ratio_

        plt.figure(figsize=(8, 6))
        plt.plot(
            range(1, self.n_components + 1),
            explained_variance * 100,
            marker="o",
            linestyle="-",
        )
        plt.xlabel("Principal Component")
        plt.ylabel("Explained Variance (%)")
        plt.title("Scree Plot")
        plt.grid(True)
        plt.legend()
        sl.pyplot(plt)
