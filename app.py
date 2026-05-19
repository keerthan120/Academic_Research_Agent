import streamlit as st
from agents import academic_coordinator

DEFAULT_MODEL = "meta-llama/llama-3-8b-instruct"

st.set_page_config(
    page_title="Academic Research Assistant",
    layout="wide"
)

st.title("Academic Research Assistant")
st.write("Search arXiv papers and generate academic analysis.")

with st.sidebar:
    st.header("Settings")
    model = st.text_input("OpenRouter Model", value=DEFAULT_MODEL)

topic = st.text_input(
    "Enter research topic",
    placeholder="Example: machine learning in healthcare"
)

if st.button("Search and Analyze"):
    if topic.strip() == "":
        st.warning("Please enter a research topic.")
    else:
        with st.spinner("Searching papers and generating analysis..."):
            papers, analysis = academic_coordinator(topic.strip(), model.strip())

        st.header("Papers")

        if len(papers) == 0:
            st.error("No papers found.")
        else:
            for i, paper in enumerate(papers, start=1):
                st.subheader(f"Paper {i}")
                st.write("**Title:**", paper["title"])
                st.write("**Authors:**", ", ".join(paper["authors"]))
                st.write("**Published:**", paper["published"])
                st.write("**URL:**", paper["url"])

                st.write("**Summary:**")
                st.info(paper["summary"])

                st.divider()

        st.header("AI Analysis")
        st.write(analysis)
