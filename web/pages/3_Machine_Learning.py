from matplotlib import pyplot as plt
import streamlit as sl
from logistic_regression_classification import LogisticRegressionClassification
from read_csv import upload_and_read_file
from knn_classification import KNNClassification
from hierarchical_clustering import HierachicalClustering
from kmeans_clustering import KMeansClustering


def main():
    # Define and create the radio buttons
    options = ["Classification Algorithms", "Clustering Algorithms"]
    selected_option = sl.sidebar.radio("Machine Learning Algorithms", options)
    # Create instances of the classes
    lr = LogisticRegressionClassification()
    knn = KNNClassification(k=5)
    hc = HierachicalClustering()
    kc = KMeansClustering()

    # Upload the file
    data_frame, class_names = upload_and_read_file()

    if data_frame.empty:
        sl.error(
            "Either the uploaded file is empty or could not be read, or Target is Empty. Please upload a valid file or input a Target."
        )
    else:

        # Use the methods of the classes
        if selected_option == "Classification Algorithms":

            if data_frame is not None:
                data_frame = lr.data_preprocess_for_the_supervised_algorithms(
                    data_frame, 0
                )
                sl.header("Settings:")

                # Get k from user
                k = sl.number_input(
                    'Specify the number of neighbours "k" for the kNN classification:',
                    min_value=1,
                    step=1,
                )

                test_size = sl.number_input(
                    "Specify the test size (0.0,0.5] for the Logistic Regression classification (We recommend to not use a test size greater than 0.2): ",
                    min_value=0.01,
                    max_value=0.5,
                    step=0.01,
                )

                training_data, testing_data = lr.data_split(data_frame, test_size)

                if test_size:
                    sl.title("Logistic Regression")
                    lr.logistic_regression(training_data, testing_data, class_names)
                    sl.markdown("---")
                if k:
                    sl.title("k-Nearest Neighbors")
                    knn.kNN_algorithm(training_data, testing_data, class_names)
                    sl.markdown("---")

        elif selected_option == "Clustering Algorithms":
            if data_frame is not None:
                sl.title("Hierachical Clustering")
                hc.hierarchical_clustering(data_frame)
                sl.markdown("---")
                sl.title("k-Means Clustering")
                kc.kmeans_algorithm(data_frame)


if __name__ == "__main__":
    main()
