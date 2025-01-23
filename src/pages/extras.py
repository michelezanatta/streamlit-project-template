# import streamlit as st
# from streamlit_extras.app_logo import add_logo
# from streamlit_extras.badges import badge
# from streamlit_extras.colored_header import colored_header
# from streamlit_extras.mention import mention
# from streamlit_extras.add_vertical_space import add_vertical_space
# from streamlit_extras.switch_page_button import switch_page
# from streamlit_extras.dataframe_explorer import dataframe_explorer
# from streamlit_extras.metric_cards import style_metric_cards
# from streamlit_extras.stateful_button import button
# from streamlit_extras.card import card

# # Import data
# @st.cache_data
# def load_data():
#     import pandas as pd
#     url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
#     return pd.read_csv(url)

# st.title("Streamlit Extras Showcase")
# st.write("This page demonstrates some of the most important components from the `streamlit-extras` library.")

# # Logo Component
# st.header("1. App Logo")
# add_logo("https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Streamlit_logo.svg/1200px-Streamlit_logo.svg.png", height=100)
# st.write("Added a logo at the top of the page.")

# # Badge Component
# st.header("2. Badges")
# badge("https://github.com/streamlit")
# badge("https://pypi.org/project/streamlit-extras", text="PyPI: Streamlit Extras", type="badge")
# st.write("Badges can display GitHub links, PyPI links, and more.")

# # Colored Header
# st.header("3. Colored Headers")
# colored_header(label="Colored Header Example", description="You can add headers with colored backgrounds.", color_name="blue-70")

# # Mention Component
# st.header("4. Mentions")
# mention("Streamlit", "https://streamlit.io", icon="🔗")

# # Add Vertical Space
# st.header("5. Vertical Spacing")
# st.write("Here's a vertical space between components:")
# add_vertical_space(3)

# # Switch Page Button
# st.header("6. Switch Page Button")
# st.write("Use this button to switch to another page:")
# if switch_page("Home"):
#     st.success("Navigated to the Home page!")


# # DataFrame Explorer
# st.header("8. DataFrame Explorer")
# df = load_data()
# filtered_data = dataframe_explorer(df)
# st.write("Filtered DataFrame:", filtered_data)

# # Metric Cards
# st.header("9. Styled Metric Cards")
# col1, col2, col3 = st.columns(3)
# col1.metric("Average Sepal Length", f"{df['sepal_length'].mean():.2f}")
# col2.metric("Average Sepal Width", f"{df['sepal_width'].mean():.2f}")
# col3.metric("Average Petal Length", f"{df['petal_length'].mean():.2f}")
# style_metric_cards()

# # Stateful Button
# st.header("10. Stateful Button")
# if button("Click Me"):
#     st.success("You clicked the stateful button!")

# # Card Component
# st.header("11. Cards")
# card(title="Card Title", text="This is a simple card example.", url="https://streamlit.io")

