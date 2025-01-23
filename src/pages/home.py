import streamlit as st

st.set_page_config(
    page_title="Homepage",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    "# Streamlit Project Template")
st.write("""This is a template for a Streamlit project. 
         It includes a sidebar navigation and a page layout. 
         You can add your own pages and content to the template.
         Every page is implemented to show a particular feature of Streamlit.""")

