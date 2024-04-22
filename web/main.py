import streamlit as sl
import pandas as pd

sidebar = sl.sidebar

sidebar.markdown("# Soft Tech 2024 Project")

button_info = sidebar.button("Info")

if button_info:
    # Will close the file after it's done reading it.
    with open("./web/info.md", "r") as file:
        markdown_info = file.read()
    sl.write(markdown_info)
