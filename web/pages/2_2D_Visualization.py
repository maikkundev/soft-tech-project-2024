import streamlit as sl
import pandas as pd
import io


def read_file(file, file_extension):
    if file_extension == "csv":
        delim = sl.selectbox(
            'Please enter the delimiter of the csv file. It must be either ";" or ",": ',
            [",", ";"],
        )
        return pd.read_csv(
            io.StringIO(file.getvalue().decode("utf-8")), delimiter=delim
        )
    else:
        return pd.read_excel(io.BytesIO(file))


uploaded_file = sl.file_uploader("Import a csv or an excel file:", type=["csv", "xlsx"])

if uploaded_file is not None:
    data = read_file(uploaded_file, uploaded_file.type.split("/")[-1])
    sl.dataframe(data)
