"""Streamlit demo: run the blog generation pipeline from a simple UI."""

import sys
from pathlib import Path

# Ensure project root is on path when running: streamlit run app.py
_project_root = Path(__file__).resolve().parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from workflows.linear_pipeline import run_linear_pipeline
from utils.markdown_exporter import export_to_markdown_file

st.set_page_config(
    page_title="Blog Generator (Linear Workflow)",
    page_icon="✍️",
    layout="wide",
)

st.title("✍️ Agentic Blog Generator")
st.caption("Linear workflow: Research → Facts → Outline → Article (LangChain + OpenAI)")

topic = st.text_input(
    "Blog topic",
    placeholder="e.g. Benefits of Python for data science",
    label_visibility="collapsed",
)
use_tavily = st.checkbox("Use Tavily web search for research (optional)", value=False)

if not topic.strip():
    st.info("Enter a topic above and click **Generate** to run the pipeline.")
    st.stop()

if st.button("Generate blog", type="primary"):
    with st.spinner("Running pipeline…"):
        progress = st.progress(0, text="Research…")
        # Run full pipeline (agents run sequentially inside)
        result = run_linear_pipeline(topic.strip(), use_tavily=use_tavily)
        progress.progress(100, text="Done.")

    tabs = st.tabs(["Article", "Outline", "Facts", "Research"])
    with tabs[0]:
        st.markdown(result["article"])
        out_name = "examples/generated_blog.md"
        export_to_markdown_file(result["article"], out_name)
        st.download_button(
            "Download as Markdown",
            data=result["article"],
            file_name="blog.md",
            mime="text/markdown",
        )
    with tabs[1]:
        st.markdown(result["outline"])
    with tabs[2]:
        st.markdown(result["facts"])
    with tabs[3]:
        st.markdown(result["research"])
