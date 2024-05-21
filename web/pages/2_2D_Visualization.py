import streamlit as sl
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import LabelEncoder
from matplotlib import pyplot as plt

import io

selection = ["Data upload", "PCA Analysis", "t-SNE Analysis"]
selected = sl.sidebar.radio("Choose an option", selection)
data = None


# Function that performs dimensionality reduction using the PCA algorithm
@sl.cache_data()
def perform_pca(data, n_components):
    pca = PCA(n_components=n_components)
    pca.fit(data)
    return pca


# Function that performs dimensionality reduction using the t-SNE algorithm
@sl.cache_data()
def perform_tSNE(df, n_components=2):
    features = df.copy()
    tsne = TSNE(n_components=n_components)
    new_features = tsne.fit_transform(features)
    return pd.DataFrame(new_features)


@sl.cache_data()
def read_file(file, file_extension, delim):
    if file_extension == "csv":
        return pd.read_csv(
            io.StringIO(file.getvalue().decode("utf-8")), delimiter=delim
        )
    else:
        return pd.read_excel(io.BytesIO(file))


def visualize_pca_scree(pca, num_components):
    explained_variance = pca.explained_variance_ratio_

    plt.figure(figsize=(8, 6))
    plt.plot(
        range(1, num_components + 1),
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


if "uploaded_file" not in sl.session_state:
    sl.session_state.uploaded_file = None

if "data" not in sl.session_state:
    sl.session_state.data = None

if selected == "Data upload":
    sl.session_state.uploaded_file = sl.file_uploader(
        "Import a csv or an excel file:", type=["csv", "xlsx"]
    )

    if sl.session_state.uploaded_file is not None:
        delim = sl.selectbox(
            'Please enter the delimiter of the csv file. It must be either ";" or ",": ',
            [",", ";"],
        )
        sl.session_state.data = read_file(
            sl.session_state.uploaded_file,
            sl.session_state.uploaded_file.type.split("/")[-1],
            delim,
        )
        le = LabelEncoder()
        sl.session_state.data["Target"] = le.fit_transform(
            sl.session_state.data["Target"]
        )

        sl.dataframe(sl.session_state.data)


elif selected == "PCA Analysis":
    sl.write("You selected PCA Analysis.")
    # Check if data is available and is a DataFrame
    if isinstance(sl.session_state.data, pd.DataFrame):
        visualize_pca_scree(perform_pca(sl.session_state.data, 3), 3)

    else:
        sl.write("Please upload your data first!")

elif selected == "t-SNE Analysis":
    sl.write("You selected t-SNE analysis")
    # Check if data is available and is a DataFrame
    if isinstance(sl.session_state.data, pd.DataFrame):
        # Perform t-SNE and plot the Dataframe
        tsne_data = perform_tSNE(sl.session_state.data, 2)
        sl.line_chart(tsne_data)
    else:
        sl.write("Please upload your data first!")
