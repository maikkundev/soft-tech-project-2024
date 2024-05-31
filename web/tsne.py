from sklearn.calibration import LabelEncoder
import streamlit as sl
import pandas as pd
from sklearn.manifold import TSNE


class tSNEDecomposition:
    def __init__(self, data_frame, n_components):
        self.data_frame = data_frame.apply(
            LabelEncoder().fit_transform
        )  # Apply label encoding
        self.n_components = n_components
        self.tsne = None

    # Function that performs dimensionality reduction using the t-SNE algorithm
    def perform_tSNE(self):
        features = self.data_frame.copy()
        self.tsne = TSNE(n_components=self.n_components)
        result = pd.DataFrame(self.tsne.fit_transform(features), columns=["PC1", "PC2"])
        sl.scatter_chart(result)
