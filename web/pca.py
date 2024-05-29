import pandas as pd
from sklearn.preprocessing import LabelEncoder
import streamlit as sl
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt


class PCADecomposition:
    def __init__(self, data_frame, n_components):
        self.data_frame = data_frame
        self.n_components = n_components
        self.pca = None

    # Function that performs dimensionality reduction using the PCA algorithm
    def perform_pca(self):
        pca = PCA(n_components=self.n_components)
        pca.fit(self.data_frame)
        sl.scatter_chart(pd.DataFrame(pca.transform(self.data_frame)))
