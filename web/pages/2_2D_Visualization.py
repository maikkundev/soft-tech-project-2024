from matplotlib import pyplot as plt
import streamlit as sl
from read_csv import upload_and_read_file
from pca import PCADecomposition
from tsne import tSNEDecomposition


def main():
    options = ["PCA Analysis", "t-SNE Analysis", "EDA"]
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
        elif selected_option == "EDA":
            # Ensure the DataFrame only contains numeric columns
            numeric_data_frame = data_frame.select_dtypes(include=["float64", "int64"])

            # Check if class_name is in numeric_data_frame columns
            if isinstance(class_name, list):
                # If class_name is a list, check if all elements are in the DataFrame's columns
                if all(name in numeric_data_frame.columns for name in class_name):
                    target = class_name
                else:
                    sl.error(
                        "Some selected targets are not numeric. Please select numeric targets for EDA."
                    )
                    return
            else:
                # If class_name is not a list, check if it's in the DataFrame's columns
                if class_name in numeric_data_frame.columns:
                    target = class_name
                else:
                    sl.error(
                        "Selected target is not numeric. Please select a numeric target for EDA."
                    )
                    return

            # Display basic statistics for the selected target
            sl.write(numeric_data_frame[target].describe())

            # Display histogram for the selected target
            fig, ax = plt.subplots()
            ax.hist(numeric_data_frame[target])
            sl.pyplot(fig)

            # Display scatter plots for the selected target against a few other features
            for column in numeric_data_frame.columns[
                :5
            ]:  # Adjust this to change the number of scatter plots
                if column != target:
                    fig, ax = plt.subplots()
                    ax.scatter(numeric_data_frame[column], numeric_data_frame[target])
                    sl.pyplot(fig)


if __name__ == "__main__":
    main()
