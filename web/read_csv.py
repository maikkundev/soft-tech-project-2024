# read_csv.py
import streamlit as sl
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import io


@sl.cache_data()
def read_file(file, file_extension, delim):
    if file_extension == "csv":
        return pd.read_csv(
            io.StringIO(file.getvalue().decode("utf-8")), delimiter=delim
        )
    else:
        return pd.read_excel(io.BytesIO(file))


def upload_and_read_file():
    uploaded_file = sl.file_uploader(
        "Import a csv or an excel file:", type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        delim = sl.selectbox(
            'Please enter the delimiter of the csv file. It must be either ";" or ",": ',
            [",", ";"],
        )
        data = read_file(
            uploaded_file,
            uploaded_file.type.split("/")[-1],
            delim,
        )
        le = LabelEncoder()
        data["Target"] = le.fit_transform(data["Target"])

        return data
