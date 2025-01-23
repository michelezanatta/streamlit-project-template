import streamlit as st
import sys
from pathlib import Path
import time
from datetime import time
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from rsc.config import config_params

data_dir = config_params.data_dir
images_dir = config_params.images_dir

st.title("Streamlit Input Widgets Showcase")
st.write("This page demonstrates various input widgets in Streamlit, categorized into sections.")


st.divider()

# Buttons Section
st.header("Buttons")
if st.button("Click Me", help = "This button will do absolutely nothing", key = "example_button", icon = "🚀"):
    st.write("Button clicked!")
else:
    st.write("Button not clicked.")

st.download_button(
    label="Download Example File",
    data="Example file content",
    file_name=f"example.txt",
    mime="text/plain",
)

with open(f"{images_dir}/example.png", "rb") as file:
    btn = st.download_button(
        label="Download Example Image",
        data=file,
        file_name="example.png",
        mime="image/png",
    )

with st.form(key="form_button_example"):
    form_input = st.text_input("Enter something:")
    submitted = st.form_submit_button("Submit Form")
    if submitted:
        st.write(f"Form submitted with input: {form_input}")

# st.write("Fragment example:")
# @st.fragment
# def release_the_balloons():
#     st.button("Release the balloons", help="Fragment rerun")
#     st.balloons()

# with st.spinner("Inflating balloons..."):
#     time.sleep(5)
# release_the_balloons()
# st.button("Inflate more balloons", help="Full rerun")


st.link_button("Go to gallery", "https://streamlit.io/gallery")

st.page_link(f"pages/home.py", label = "Go to home page", icon = "🏠")

st.divider()

# Selection Widgets Section
st.header("Selection Widgets")
check = st.checkbox("Check Me", value=False)
if check:
    st.write("Checkbox checked!")
else:
    st.write("Checkbox not checked.")

color = st.color_picker("Pick A Color", "#00f900")
st.write("The current color is", color)

sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")

st.multiselect(
    "Select Multiple Options",
    options=["Option 1", "Option 2", "Option 3"],
    default=["Option 1"],
)

option_map = {
    0: ":material/add:",
    1: ":material/zoom_in:",
    2: ":material/zoom_out:",
    3: ":material/zoom_out_map:",
}
selection = st.pills(
    "Tool",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
)
st.write(
    "Your selected option: "
    f"{None if selection is None else option_map[selection]}"
)

genre = st.radio(
    "What's your favorite movie genre",
    [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
    captions=[
        "Laugh out loud.",
        "Get the popcorn.",
        "Never stop learning.",
    ],
)

if genre == ":rainbow[Comedy]":
    st.write("You selected comedy.")
else:
    st.write("You didn't select comedy.")

option_map = {
    0: ":material/add:",
    1: ":material/zoom_in:",
    2: ":material/zoom_out:",
    3: ":material/zoom_out_map:",
}
selection = st.segmented_control(
    "Tool",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
)
st.write(
    "Your selected option: "
    f"{None if selection is None else option_map[selection]}"
)

st.select_slider(
    "Select a Range",
    options=["Low", "Medium", "High"],
    value=("Medium"),
)

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:
    st.checkbox("Disable selectbox widget", key="disabled")
    st.radio(
        "Set selectbox label visibility 👉",
        key="visibility",
        options=["visible", "hidden", "collapsed"],
    )

with col2:
    option = st.selectbox(
        "How would you like to be contacted?",
        ("Email", "Home phone", "Mobile phone"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )

on = st.toggle("Activate feature")

if on:
    st.write("Feature activated!")

st.divider()
# Numeric Widgets Section
st.header("Numeric Inputs")
st.number_input(
    "Input a Number",
    min_value=0,
    max_value=100,
    value=50,
    step=1,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.text("Slider with number")
    st.slider(
        "Adjust a Slider",
        min_value=0,
        max_value=100,
        value=25,
        step=5,
    )
with col2:
    st.text("Slider with date")
    appointment = st.slider(
        "Schedule your appointment:", value=(time(11, 30), time(12, 45))
    )
    st.write("You're scheduled for:", appointment)
with col3:
    st.text("Slider with time")
    start_time = st.slider(
        "When do you start?",
        value=datetime(2020, 1, 1, 9, 30),
        format="MM/DD/YY - hh:mm",
    )
    st.write("Start time:", start_time)

st.divider()

# Date and Time Widgets Section
st.header("Date and Time Inputs")
st.date_input("Pick a Date", value=None)

st.time_input("Pick a Time", value=None)

st.divider()

# Text Inputs Section
st.header("Text Inputs")
title = st.text_input("Movie title", "Life of Brian")
st.write("The current movie title is", title)

txt = st.text_area(
    "Text to analyze",
    "It was the best of times, it was the worst of times, it was the age of "
    "wisdom, it was the age of foolishness, it was the epoch of belief, it "
    "was the epoch of incredulity, it was the season of Light, it was the "
    "season of Darkness, it was the spring of hope, it was the winter of "
    "despair, (...)",
)

st.write(f"You wrote {len(txt)} characters.")


st.divider()
# Other Widgets Section
st.header("Other Widgets")

st.file_uploader("Upload a File", type=["csv", "txt", "png", "jpg"])

enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

st.link_button("Go to camera input documentation", "https://docs.streamlit.io/develop/api-reference/widgets/st.camera_input")

if picture:
    st.image(picture)

enable_mic = st.checkbox("Enable microphone", key = "enable_mic")
if enable_mic:
    audio_value = st.audio_input("Record a voice message", key = "audio")
    if audio_value:
        st.audio(audio_value)