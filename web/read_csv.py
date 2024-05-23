# read_csv.py
import streamlit as sl
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import io


@sl.cache_data()
# Funtion to read the file based on its extension.
def read_file(filename, file_extension):
    if file_extension == "csv":
        for delim in [";", ","]:
            try:
                data = pd.read_csv(filename, delimiter=delim)
                if len(data.columns) > 1:
                    return data
            except pd.errors.EmptyDataError:
                continue
        sl.error(
            'The file you provided uses an invalid delimiter. Modify the delimiter either to ";" or to ",".'
        )
    else:
        return pd.read_excel(filename)


def upload_and_read_file():

    uploaded_file = sl.file_uploader(
        "Import a csv or an excel file:", type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        data = read_file(
            uploaded_file,
            uploaded_file.type.split("/")[-1],
        )

        target = sl.text_input("Please specify your Target")

        if target is not None and target != "":

            # Get class names before encoding
            class_mapping = data[target].unique()

            # Fit the LabelEncoder and get the mapping
            le = LabelEncoder()
            le.fit(data[target])
            class_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
            # Sort class_mapping by values to get a list of class names
            class_names = [
                k for k, v in sorted(class_mapping.items(), key=lambda item: item[1])
            ]

            data["Target"] = le.transform(data[target])

            return data, class_names

    # Return empty DataFrame and list if no file is uploaded or target is not specified
    return pd.DataFrame(), []
