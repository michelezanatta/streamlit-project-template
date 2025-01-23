import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from bokeh.plotting import figure
import altair as alt
import pydeck as pdk
from streamlit_folium import st_folium
import folium
from sklearn.datasets import load_iris
import graphviz
import numpy as np

# Load the Iris dataset
def load_iris_data():
    iris = load_iris(as_frame=True)
    df = iris.frame
    df['species'] = df['target'].map(dict(enumerate(iris.target_names)))
    return df

df = load_iris_data()

st.title("Plot Display Showcase")
st.write("This page demonstrates visualizations using various plotting libraries.")

# Plotly
st.header("Plotly Example")
st.write("Scatter plot with Plotly:")
fig_plotly = px.scatter(
    df,
    x="sepal length (cm)",
    y="sepal width (cm)",
    color="species",
    title="Sepal Length vs Width (Plotly)"
)
st.plotly_chart(fig_plotly)

# Seaborn and Matplotlib
st.header("Seaborn and Matplotlib Example")
st.write("Pairplot using Seaborn:")
sns_plot = sns.pairplot(df, hue="species")
st.pyplot(sns_plot)

# # Bokeh
# st.header("Bokeh Example")
# st.write("Interactive Bokeh plot:")
# bokeh_fig = figure(title="Sepal Length vs Width (Bokeh)", x_axis_label="Sepal Length", y_axis_label="Sepal Width")
# bokeh_fig.circle(df["sepal length (cm)"], df["sepal width (cm)"], size=8, color="navy", alpha=0.5)
# st.bokeh_chart(bokeh_fig)

# Altair
st.header("Altair Example")
st.write("Altair scatter plot:")
alt_chart = alt.Chart(df).mark_circle(size=60).encode(
    x="sepal length (cm)",
    y="sepal width (cm)",
    color="species",
    tooltip=["sepal length (cm)", "sepal width (cm)", "species"]
).interactive()
st.altair_chart(alt_chart, use_container_width=True)

# Pydeck
st.header("Pydeck Example")
st.write("Pydeck geographical plot (dummy coordinates for illustration):")
df_geo = df.copy()
df_geo["lat"] = 37.7749  # Latitude for San Francisco
df_geo["lon"] = -122.4194  # Longitude for San Francisco
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_geo,
    get_position="[lon, lat]",
    get_radius=100000,
    get_fill_color=[180, 0, 200, 140],
    pickable=True,
)
view_state = pdk.ViewState(latitude=37.7749, longitude=-122.4194, zoom=8)
r = pdk.Deck(layers=[layer], initial_view_state=view_state)
st.pydeck_chart(r)

# Streamlit st.map
st.header("Streamlit Map Example")
st.write("Map with `st.map` (using dummy coordinates):")
st.map(df_geo[["lat", "lon"]])

# st-folium
st.header("st-folium Example")
st.write("Interactive map with Folium:")
folium_map = folium.Map(location=[37.7749, -122.4194], zoom_start=12)
for _, row in df_geo.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=10,
        popup=row["species"],
        color="blue",
        fill=True,
        fill_color="blue"
    ).add_to(folium_map)
st_folium(folium_map, width=700)

# Graphviz
st.header("Graphviz Example")
st.write("Simple graph with Graphviz:")
graph = graphviz.Digraph()
graph.edge("Sepal Length", "Sepal Width")
graph.edge("Petal Length", "Petal Width")
graph.edge("Species", "Petal Width")
st.graphviz_chart(graph)


# Altair Chart with Selection
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        np.random.randn(20, 3), columns=["a", "b", "c"]
    )
df = st.session_state.data

point_selector = alt.selection_point("point_selection")
interval_selector = alt.selection_interval("interval_selection")
chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x="a",
        y="b",
        size="c",
        color="c",
        tooltip=["a", "b", "c"],
        fillOpacity=alt.condition(point_selector, alt.value(1), alt.value(0.3)),
    )
    .add_params(point_selector, interval_selector)
)

event = st.altair_chart(chart, key="alt_chart", on_select="rerun")

event