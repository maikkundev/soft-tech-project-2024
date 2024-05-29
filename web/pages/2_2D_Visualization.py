from matplotlib import pyplot as plt
import pandas as pd
import streamlit as sl
from read_csv import upload_and_read_file
from pca import PCADecomposition
from tsne import tSNEDecomposition
import seaborn as sns


def main():
    options = ["PCA & t-SNE Analysis", "EDA"]
    selected_option = sl.sidebar.radio("Choose an option", options)

    data_frame, class_name = upload_and_read_file(read_all_classes=True)

    if data_frame.empty:
        sl.warning(
            "Either the uploaded file is empty or could not be read, or Target is Empty. Please upload a valid file or input a Target."
        )
    else:
        pca = PCADecomposition(data_frame, 2)
        tsne = tSNEDecomposition(data_frame, 2)
        if selected_option == "PCA & t-SNE Analysis":
            sl.header("PCA")
            pca.perform_pca()
            sl.header("t-SNE")
            tsne.perform_tSNE()
        elif selected_option == "EDA":
            # Select a target for EDA
            eda_target = sl.selectbox(
                "Please specify a target to perform EDA", data_frame.columns
            )

            # Display histogram for the target
            fig, ax = plt.subplots()
            sns.histplot(data_frame[eda_target], kde=False, bins=30, ax=ax)
            sl.pyplot(fig)

            # Display box plot for the target if it's numeric
            if pd.api.types.is_numeric_dtype(data_frame[eda_target]):
                fig, ax = plt.subplots()
                sns.boxplot(x=data_frame[eda_target], ax=ax)
                sl.pyplot(fig)


if __name__ == "__main__":
    main()
