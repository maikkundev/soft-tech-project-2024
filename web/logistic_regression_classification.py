from matplotlib import pyplot as plt
import streamlit as sl
import seaborn as sns
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import f_classif
from sklearn.model_selection import train_test_split


class LogisticRegressionClassification:
    def __init__(self):
        pass

    # Function that fills the missing values with the mean of the variables
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

    # Function that removes the outliers
    def remove_outliers_iqr(self, df, iqr_factor=1.5):
        conditions = []
        for col in df.columns[:-1]:
            lower_bound = df[col].quantile(5 / 100)
            upper_bound = df[col].quantile(95 / 100)
            condition = (df[col] < lower_bound) | (df[col] > upper_bound)
            conditions.append(condition)

        combined_condition = ~pd.concat(conditions, axis=1).any(axis=1)
        return df[combined_condition]

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
            X, y, test_size=test_size, random_state=42
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

    # Function that implements the Logistic regression classification algorithm
    def logistic_regression(
        self, training_data, testing_data, class_names, random_state=None
    ):
        X_train, y_train = training_data.iloc[:, :-1], training_data.iloc[:, -1]
        X_test, y_test = testing_data.iloc[:, :-1], testing_data.iloc[:, -1]
        unique_classes = y_train.unique()
        X_train = X_train.values
        X_test = X_test.values

        model = LogisticRegression(random_state=random_state)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        accuracy = round((accuracy_score(y_test, y_pred) * 100), 2)
        precision = round(
            (
                precision_score(y_test, y_pred, labels=unique_classes, average="micro")
                * 100
            ),
            2,
        )
        recall = round(
            (
                recall_score(y_test, y_pred, labels=unique_classes, average="micro")
                * 100
            ),
            2,
        )
        cm = confusion_matrix(y_test, y_pred, labels=unique_classes)
        f1 = round((f1_score(y_test, y_pred, average="micro") * 100), 3)

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

        return accuracy, precision, recall, f1
