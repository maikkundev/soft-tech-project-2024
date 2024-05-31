from matplotlib import pyplot as plt
import streamlit as sl
from logistic_regression_classification import LogisticRegressionClassification
from read_csv import upload_and_read_file
from knn_classification import KNNClassification
from hierarchical_clustering import HierachicalClustering
from kmeans_clustering import KMeansClustering


def main():
    sl.set_page_config(page_title="Machine Learning", page_icon="🤖")

    options = ["Classification Algorithms", "Clustering Algorithms"]
    selected_option = sl.sidebar.radio("Machine Learning Algorithms", options)

    lr = LogisticRegressionClassification()
    hc = HierachicalClustering()
    kc = KMeansClustering()

    # Upload the file
    data_frame, class_names = upload_and_read_file(read_all_classes=False)

    if data_frame is not None and data_frame.empty:
        sl.warning(
            "Either the uploaded file is empty or could not be read, or Target is Empty. Please upload a valid file or input a Target."
        )
    else:

        # Use the methods of the classes
        if selected_option == "Classification Algorithms":

            if data_frame is not None:
                data_frame = lr.data_preprocess_for_the_supervised_algorithms(
                    data_frame, 0
                )

                sl.title("Logistic Regression")
                test_size = sl.number_input(
                    "Specify the test size (0.0,0.5] for the Logistic Regression classification (We recommend to not use a test size greater than 0.2): ",
                    min_value=0.01,
                    max_value=0.5,
                    step=0.01,
                )

                if test_size:
                    training_data, testing_data = lr.data_split(data_frame, test_size)
                    lr_a, lr_p, lr_r, lr_f1 = lr.logistic_regression(
                        training_data, testing_data, class_names
                    )
                    sl.markdown("---")

                sl.title("k-Nearest Neighbors")
                # Get k from user
                k = sl.number_input(
                    'Specify the number of neighbours "k" for the kNN classification:',
                    min_value=1,
                    step=1,
                )

                if k:
                    knn = KNNClassification(k=k)
                    training_data, testing_data = knn.data_split(data_frame, k)
                    knn_a, knn_p, knn_r, knn_f1 = knn.kNN_algorithm(
                        training_data, testing_data, class_names
                    )
                    sl.markdown("---")

                if k and test_size:
                    best_accuracy = max(knn_a, lr_a), (
                        lambda knn_a, lr_a: (
                            "(KNN)" if knn_a > lr_a else "(Logistic Regression)"
                        )
                    )(knn_a, lr_a)
                    best_precision = max(knn_p, lr_p), (
                        lambda knn_p, lr_p: (
                            "(KNN)" if knn_p > lr_p else "(Logistic Regression)"
                        )
                    )(knn_p, lr_p)
                    best_recall = max(knn_r, lr_r), (
                        lambda knn_r, lr_r: (
                            "(KNN)" if knn_r > lr_r else "(Logistic Regression)"
                        )
                    )(knn_r, lr_r)
                    best_f1 = max(knn_f1, lr_f1), (
                        lambda knn_f1, lr_f1: (
                            "(KNN)" if knn_f1 > lr_f1 else "(Logistic Regression)"
                        )
                    )(knn_f1, lr_f1)

                    sl.header("Best results")
                    sl.write(
                        "Accuracy: {0} {1}".format(best_accuracy[0], best_accuracy[1])
                    )
                    sl.write(
                        "Precision: {0} {1}".format(
                            best_precision[0], best_precision[1]
                        )
                    )
                    sl.write("Recall: {0} {1}".format(best_recall[0], best_recall[1]))
                    sl.write("F1 Score: {0} {1}".format(best_f1[0], best_f1[1]))

        elif selected_option == "Clustering Algorithms":
            if data_frame is not None:
                sl.title("Hierarchical Clustering")
                hc_s = hc.hierarchical_clustering(data_frame)
                sl.markdown("---")
                sl.title("k-Means Clustering")
                kc_s = kc.kmeans_algorithm(data_frame)

                sl.header("Best Results")
                best_silhouette = max(hc_s, kc_s), (
                    lambda hc_s, kc_s: (
                        "(Hierachical Clustering)"
                        if hc_s > kc_s
                        else "(k-Means Clustering)"
                    )
                )(hc_s, kc_s)
                sl.write(
                    "Silhouette Score: {0} {1}".format(
                        best_silhouette[0], best_silhouette[1]
                    )
                )


if __name__ == "__main__":
    main()
