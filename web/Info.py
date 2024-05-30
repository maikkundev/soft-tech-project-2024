import streamlit as sl

sl.set_page_config(page_title="Welcome", page_icon="👋")

# Will close the file after it's done reading it.
with open("./web/info.md", "r") as file:
    markdown_info = file.read()
sl.write(markdown_info)
