import pandas as pd
from sklearn.preprocessing import LabelEncoder
import streamlit as sl
from sklearn.decomposition import PCA


class PCADecomposition:
    def __init__(self, data_frame, n_components):
        self.data_frame = data_frame.apply(
            LabelEncoder().fit_transform
        )  # Apply label encoding
        self.n_components = n_components
        self.pca = None

    # Function that performs dimensionality reduction using the PCA algorithm
    def perform_pca(self):
        pca = PCA(n_components=self.n_components)
        pca.fit(self.data_frame)
        # pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
        result = pd.DataFrame(pca.transform(self.data_frame), columns=["PC1", "PC2"])
        sl.scatter_chart(result)
