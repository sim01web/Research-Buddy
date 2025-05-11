from typing import Dict
from pathlib import Path
import google.generativeai as genai
import sys
sys.path.append(str(Path(__file__).resolve().parents[1])) 
# Load Gemini API key from config
from app.config import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

# Load critique prompt template
PROMPT_PATH = Path(__file__).resolve().parents[1] / 'prompts' / 'critique_prompt.txt'
CRITIQUE_PROMPT_TEMPLATE = PROMPT_PATH.read_text()

def critique_summary(summary: str) -> str:
    """
    Uses Gemini to critique the generated summary based on completeness, clarity, and scientific depth.
    """
    prompt = CRITIQUE_PROMPT_TEMPLATE.replace("{{summary}}", summary)
    model = genai.GenerativeModel("gemma-3-27b-it")
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    from agents.summarize_agent import summarize_paper
    from agents.search_agent import search_arxiv

    papers = search_arxiv("aspect based sentiment analysis", max_results=1)
    summary = summarize_paper(papers[0])
    critique = critique_summary(summary)

    print("\nGenerated Summary:\n", summary)
    print("\nCritique:\n", critique)
