import streamlit as st
from agents import academic_coordinator

DEFAULT_MODEL = "meta-llama/llama-3-8b-instruct"

st.set_page_config(
    page_title="Academic Research Assistant",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

.title {
    font-size: 38px;
    font-weight: 800;
    color: #1f2937;
}

.subtitle {
    font-size: 17px;
    color: #4b5563;
    margin-bottom: 25px;
}

.paper-header {
    font-size: 18px;
    font-weight: 700;
    color: #111827;
}

.meta {
    color: #4b5563;
    font-size: 14px;
}

.summary-box {
    background-color: #f9fafb;
    padding: 14px;
    border-radius: 8px;
    border: 1px solid #e5e7eb;
    color: #111827;
    line-height: 1.6;
}

.analysis-box {
    background-color: #ffffff;
    padding: 22px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    color: #111827;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Academic Research Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Search research papers from arXiv and generate AI-powered academic analysis.</div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("Settings")
    model = st.text_input("OpenRouter Model", value=DEFAULT_MODEL)

topic = st.text_input(
    "Enter research topic",
    placeholder="Example: artificial intelligence in healthcare"
)

if st.button("Search and Analyze", type="primary"):
    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    with st.spinner("Searching papers and generating analysis..."):
        papers, analysis = academic_coordinator(topic.strip(), model.strip())

    st.divider()

    st.subheader("Papers")

    if not papers:
        st.error("No papers found.")
    else:
        for i, paper in enumerate(papers, start=1):
            with st.expander(f"Paper {i}: {paper['title']}", expanded=True):
                st.markdown(f'<div class="paper-header">{paper["title"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<p class="meta"><b>Authors:</b> {", ".join(paper["authors"])}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="meta"><b>Published:</b> {paper["published"]}</p>', unsafe_allow_html=True)
                st.markdown(f'**URL:** [{paper["url"]}]({paper["url"]})')

                st.markdown("**Summary:**")
                st.markdown(
                    f'<div class="summary-box">{paper["summary"]}</div>',
                    unsafe_allow_html=True
                )

    st.subheader("AI Analysis")

    st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
    st.markdown(analysis)
    st.markdown('</div>', unsafe_allow_html=True)
