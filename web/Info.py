import streamlit as sl

sl.set_page_config(page_title="Welcome", page_icon="👋")

# Will close the file after it's done reading it.
with open("./web/info.md", "r", encoding="utf-8") as file:
    markdown_info = file.read()
sl.markdown(markdown_info)
