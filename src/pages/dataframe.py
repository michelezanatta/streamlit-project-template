import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
# from pandas_profiling import ProfileReport
# from streamlit_pandas_profiling import st_profile_report

# Load Iris dataset
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    df = pd.read_csv(url)
    return df

st.title("Data Elements Showcase with Iris Dataset")
st.write("This page demonstrates various data-related components in Streamlit.")

# Load the Iris dataset
df = load_data()

# Display the raw DataFrame
st.header("DataFrame Display")
st.write("Here is the raw Iris dataset:")
st.dataframe(df)

# st.header("Pandas Profiling")
# iris_profiler = ProfileReport(df, explorative=True)
# st_profile_report(penguin_profile)

# Data Editor
st.header("Data Editor")
st.write("This is a data editor where you can edit the dataset:")
edited_df = st.data_editor(df, num_rows="dynamic", column_config={
    'species': st.column_config.SelectboxColumn("Species", options=df['species'].unique().tolist()),
    'sepal_length': st.column_config.NumberColumn("Sepal Length"),
    'sepal_width': st.column_config.NumberColumn("Sepal Width"),
    'petal_length': st.column_config.NumberColumn("Petal Length"),
    'petal_width': st.column_config.NumberColumn("Petal Width")
})
st.write("Edited DataFrame:")
st.dataframe(edited_df)

# Table Display
st.header("Table Display")
st.write("Here's a table using `st.table` to show the first few rows:")
st.table(df.head())

# Metrics
st.header("Metrics")
st.write("Displaying some metrics for the Iris dataset:")
sepal_length_avg = df["sepal_length"].mean()
sepal_width_avg = df["sepal_width"].mean()
petal_length_avg = df["petal_length"].mean()
petal_width_avg = df["petal_width"].mean()

st.metric(label="Avg Sepal Length", value=f"{sepal_length_avg:.2f}")
st.metric(label="Avg Sepal Width", value=f"{sepal_width_avg:.2f}")
st.metric(label="Avg Petal Length", value=f"{petal_length_avg:.2f}")
st.metric(label="Avg Petal Width", value=f"{petal_width_avg:.2f}")

# AgGrid
st.header("AgGrid Display")
st.write("Here's the dataset displayed using AgGrid for an interactive table:")
grid_options = GridOptionsBuilder.from_dataframe(df)
grid_options.configure_pagination(paginationPageSize=10)  # Configure pagination
grid_options.configure_default_column(editable=True, groupable=True, sortable=True)  # Set default properties for all columns
grid_options.configure_selection('multiple', use_checkbox=True)  # Enable row selection
grid_options.configure_column('species', editable=False)  # Make species column non-editable

aggrid = AgGrid(df, gridOptions=grid_options.build(), height=400, fit_columns_on_grid_load=True)
st.write("You can interact with the table above (e.g., sort, filter, select rows).")
