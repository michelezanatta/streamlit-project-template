import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from rsc.config import config_params

images_dir = config_params.images_dir


st.title("Media Elements Showcase")
st.write("This page demonstrates how to use media components in Streamlit.")

# Image Display
st.header("Image Display")
st.write("You can display images using `st.image`.")
st.image(
    f"{images_dir}/example.png",
    caption="This is a sample image",
    width=300,
    
)

# Video Display
st.header("Video Display")
st.write("You can display videos using `st.video`.")
st.video(
    "https://www.w3schools.com/html/mov_bbb.mp4",
    start_time=5,
)

# Logo Display
st.header("Logo Display")
st.write("You can display logos or smaller images in specific sections.")
st.logo(
    f"{images_dir}/example.png", icon_image=f"{images_dir}/example.png"
)

# Audio Playback
st.header("Audio Playback")
st.write("You can play audio files using `st.audio`.")
st.audio(
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    format="audio/mp3",
)
