import streamlit as st
from transformers import pipeline

# st.title("Hugging Face Demo")
# text = st.text_input("Enter text to analyze")
# @st.cache_resource()
# def get_model():
#     return pipeline("sentiment-analysis")
# model = get_model()
# if text:
#     result = model(text)
#     st.write("Sentiment:", result[0]["label"])
#     st.write("Confidence:", result[0]["score"])

st.title("Hugging Face Summarization Demo")

# # Input Text
# text = st.text_area(
#     "Enter text to summarize",
#     height=200,
#     help="Paste a paragraph or an article to summarize.",
# )

# @st.cache_resource()
# def get_summarizer():
#     # Load the summarization pipeline (runs with default backend)
#     return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# summarizer = get_summarizer()

# if text:
#     # Generate summary
#     with st.spinner("Summarizing..."):
#         summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
#     st.subheader("Summary")
#     st.write(summary[0]["summary_text"])