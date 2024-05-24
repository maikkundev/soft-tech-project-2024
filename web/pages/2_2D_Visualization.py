import streamlit as sl
from read_csv import upload_and_read_file
from pca import PCADecomposition
from tsne import tSNEDecomposition


def main():
    options = ["PCA Analysis", "t-SNE Analysis"]
    selected_option = sl.sidebar.radio("Choose an option", options)

    data_frame, class_name = upload_and_read_file()

    if data_frame.empty:
        sl.warning(
            "Either the uploaded file is empty or could not be read, or Target is Empty. Please upload a valid file or input a Target."
        )
    else:
        pca = PCADecomposition(data_frame, 3)
        tsne = tSNEDecomposition(data_frame, 3)
        if selected_option == "PCA Analysis":
            pca.visualize_pca_scree()

        elif selected_option == "t-SNE Analysis":
            tsne.perform_tSNE()


if __name__ == "__main__":
    main()
