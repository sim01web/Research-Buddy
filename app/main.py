import streamlit as st
from pathlib import Path
from fpdf import FPDF
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from agents.search_agent import search_arxiv
from agents.summarize_agent import summarize_paper
from agents.critique_agent import critique_summary
from agents.synthesis_agent import synthesize_insights
from agents.insight_agent import generate_insights
 

st.set_page_config(page_title="Research Buddy", layout="wide")
st.title("🧠 Research Buddy: AI Literature Agent")

query = st.text_input("Enter your research topic/query:", "aspect based sentiment analysis")
num_results = st.slider("Number of papers to search:", 1, 10, 3)

if st.button("Run Research Agent"):
    with st.spinner("Searching ArXiv and analyzing..."):
        papers = search_arxiv(query, max_results=num_results)

        summaries = []
        critiques = []

        for i, paper in enumerate(papers):
            st.subheader(f"📄 Paper {i+1}: {paper['title']}")
            summary = summarize_paper(paper)
            summaries.append(summary)
            st.markdown(f"**Summary:** {summary}")

            critique = critique_summary(summary)
            critiques.append(critique)
            st.markdown(f"**Critique:** {critique}")

        synthesis = synthesize_insights(summaries)
        st.subheader("🔗 Synthesized Insights")
        st.markdown(synthesis)

        insights = generate_insights(synthesis)
        st.subheader("🚀 Research Directions")
        st.markdown(insights)

        # Store in session state
        st.session_state["summaries"] = summaries
        st.session_state["critiques"] = critiques
        st.session_state["synthesis"] = synthesis

# Function to sanitize text by replacing non-ASCII characters
def sanitize_text(text: str) -> str:
    # Replace non-ASCII characters with a placeholder (e.g., '?')
    return text.encode('latin-1', 'replace').decode('latin-1')

def create_pdf(summary: str, synthesis: str, critique: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    pdf.cell(0, 10, "Research Buddy Report", ln=True)
    pdf.ln()

    # Sanitize the text content before passing it to FPDF
    summary = sanitize_text(summary)
    synthesis = sanitize_text(synthesis)
    critique = sanitize_text(critique)

    # Add sanitized text to PDF
    pdf.multi_cell(0, 10, summary or "No summary")
    pdf.multi_cell(0, 10, synthesis or "No synthesis")
    pdf.multi_cell(0, 10, critique or "No critique")

    return pdf.output(dest='S').encode('latin-1')

# Add a download button in your Streamlit app
if st.button("📄 Export as PDF"):
    if (
        "summaries" in st.session_state
        and "critiques" in st.session_state
        and "synthesis" in st.session_state
    ):
        pdf_data = create_pdf(
            "\n\n".join(st.session_state["summaries"]),
            st.session_state["synthesis"],
            "\n\n".join(st.session_state["critiques"]),
        )
        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name="research_buddy_report.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Please run the research agent first.")

