# Function that fills the missing values with the mean of the variables
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.discriminant_analysis import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import f_classif
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import streamlit as sl
import seaborn as sns


class KNNClassification:
    def __init__(self, k):
        self.k = k

    def fill_missing_values(self, df):
        features_df = df.iloc[:, :-1]
        target_df = df.iloc[:, -1]
        features_df = features_df.fillna(features_df.mean())
        df_filled = pd.concat([features_df, target_df], axis=1)
        return df_filled

    # Function that removes the duplicate instances
    def remove_duplicates(self, data):
        df_without_duplicates = data.drop_duplicates()
        return df_without_duplicates

    def remove_outliers_iqr(self, data):
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        Q1 = data[numeric_cols].quantile(0.25)
        Q3 = data[numeric_cols].quantile(0.75)
        IQR = Q3 - Q1
        conditions = [
            (data[col] < (Q1[col] - 1.5 * IQR[col]))
            | (data[col] > (Q3[col] + 1.5 * IQR[col]))
            for col in numeric_cols
        ]
        if conditions:
            combined_condition = ~pd.concat(conditions, axis=1).any(axis=1)
            return data[combined_condition]
        else:
            return data

    # Function that standardizes the data
    def data_standardization(self, df):
        scaler = StandardScaler()
        for column in df.columns[:-1]:
            df[column] = scaler.fit_transform(df[[column]])[:, 0]
        return df

    # Function that balances the data using the Synthetic over sampling technique (SMOTE)
    def balance_with_smote(self, df):
        X = df.drop(df.columns[-1], axis=1)
        y = df[df.columns[-1]]
        smote = SMOTE()
        X_resampled, y_resampled = smote.fit_resample(X, y)
        df_balanced = pd.concat([pd.DataFrame(X_resampled), y_resampled], axis=1)
        df_balanced.columns = df.columns
        return df_balanced

    # Function that performs filter based feature selection based the f-statistic and chooses the top 10 features
    def feature_selection(self, training_data):
        constant_features = training_data.columns[training_data.nunique() == 1]
        training_data.drop(constant_features, axis=1, inplace=True)
        X = training_data.drop(training_data.columns[-1], axis=1)
        y = training_data[training_data.columns[-1]]
        f_values, p_values = f_classif(X, y)
        features_importance = pd.Series(f_values, index=X.columns)
        features_importance_sorted = features_importance.sort_values(ascending=False)
        best_features = features_importance_sorted.index[:10]
        return training_data[list(best_features) + [training_data.columns[-1]]]

    # Function to split the data
    def data_split(self, data_frame, test_size):
        X = data_frame.iloc[:, :-1]
        y = data_frame.iloc[:, -1]
        unique_classes = y.unique()
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        training_data = pd.concat([X_train, y_train], axis=1)
        testing_data = pd.concat([X_test, y_test], axis=1)
        training_data = self.data_preprocess_for_the_supervised_algorithms(
            training_data, 1
        )
        return training_data, testing_data

    # Function for the preprocess of the data
    def data_preprocess_for_the_supervised_algorithms(self, data, flag):
        if flag == 0:
            data = self.fill_missing_values(data)
            data = self.remove_duplicates(data)
            data = self.remove_outliers_iqr(data)
            data = self.data_standardization(data)
            data = self.feature_selection(data)
        if flag == 1:
            data = self.balance_with_smote(data)
        return data

    def kNN_algorithm(self, training_data, testing_data, class_names):
        # Separate the features from the target variable in the training data
        X_train = training_data.iloc[:, :-1]
        y_train = training_data.iloc[:, -1]

        # Separate the features from the target variable in the testing data
        X_test = testing_data.iloc[:, :-1]
        y_test = testing_data.iloc[:, -1]

        # Create the kNN classifier
        classifier = KNeighborsClassifier(n_neighbors=self.k)

        # Train the classifier
        classifier.fit(X_train, y_train)

        # Make predictions on the testing data
        y_pred = classifier.predict(X_test)

        # Calculate and display the accuracy, precision, recall, and F1 score
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average="micro")
        recall = recall_score(y_test, y_pred, average="micro")
        f1 = f1_score(y_test, y_pred, average="micro")

        # Calculate the confusion matrix
        cm = confusion_matrix(y_test, y_pred)

        # Plot the confusion matrix
        plt.figure(figsize=(10, 7))
        sns.heatmap(
            cm, annot=True, fmt="d", xticklabels=class_names, yticklabels=class_names
        )
        plt.xlabel("Predicted")
        plt.ylabel("Truth")

        sl.pyplot(plt)

        sl.write(f"Accuracy: {accuracy}")
        sl.write(f"Precision: {precision}")
        sl.write(f"Recall: {recall}")
        sl.write(f"F1 Score: {f1}")
