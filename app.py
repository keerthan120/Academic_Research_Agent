import streamlit as st
from agents import academic_coordinator

DEFAULT_MODEL = "meta-llama/llama-3-8b-instruct"

st.set_page_config(
    page_title="Academic Research Assistant",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}

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

.paper-card {
    background: white;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    margin-bottom: 16px;
}

.paper-title {
    font-size: 20px;
    font-weight: 700;
    color: #111827;
}

.meta {
    color: #6b7280;
    font-size: 14px;
}

.analysis-box {
    background: #ffffff;
    padding: 22px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Academic Research Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Search research papers from arXiv and generate an AI-powered academic analysis.</div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("Settings")
    model = st.text_input("OpenRouter Model", value=DEFAULT_MODEL)
    st.info("Make sure your OPENROUTER_API_KEY is saved in your .env file.")

topic = st.text_input(
    "Enter research topic",
    placeholder="Example: artificial intelligence in healthcare"
)

search_button = st.button("Search and Analyze", type="primary")

if search_button:
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
            st.markdown(f"""
            <div class="paper-card">
                <div class="paper-title">Paper {i}: {paper["title"]}</div>
                <p class="meta"><b>Authors:</b> {", ".join(paper["authors"])}</p>
                <p class="meta"><b>Published:</b> {paper["published"]}</p>
                <p><b>URL:</b> <a href="{paper["url"]}" target="_blank">{paper["url"]}</a></p>
                <p><b>Summary:</b></p>
                <p>{paper["summary"]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.subheader("AI Analysis")

    st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
    st.markdown(analysis)
    st.markdown('</div>', unsafe_allow_html=True)
