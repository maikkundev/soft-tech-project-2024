import streamlit as sl
import pandas as pd

# Define and create the radio buttons
options = ["Classification Algorithms", "Clustering Algorithms"]
selected_option = sl.sidebar.radio("Machine Learning Algorithms", options)

# Display the selected option
if selected_option == "Classification Algorithms":
    sl.write("You selected classification algorithms.")
    # TODO

elif selected_option == "Clustering Algorithms":
    sl.write("You selected clustering algorithms.")
    # TODO
