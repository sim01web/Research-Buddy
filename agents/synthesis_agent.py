from typing import List, Dict
from pathlib import Path
import google.generativeai as genai
import sys
sys.path.append(str(Path(__file__).resolve().parents[1])) 
# Load Gemini API key
from app.config import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

# Load synthesis prompt
PROMPT_PATH = Path(__file__).resolve().parents[1] / 'prompts' / 'synthesis_prompt.txt'
SYNTHESIS_PROMPT_TEMPLATE = PROMPT_PATH.read_text()

def synthesize_insights(summaries: List[str]) -> str:
    """
    Uses Gemini to synthesize insights from multiple paper summaries.
    """
    joined_summaries = "\n\n".join(summaries)
    prompt = SYNTHESIS_PROMPT_TEMPLATE.replace("{{summaries}}", joined_summaries)
    model = genai.GenerativeModel("gemma-3-27b-it")
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    from agents.search_agent import search_arxiv
    from agents.summarize_agent import summarize_paper

    papers = search_arxiv("aspect based sentiment analysis", max_results=3)
    summaries = [summarize_paper(paper) for paper in papers]
    synthesis = synthesize_insights(summaries)

    print("\nIndividual Summaries:\n")
    for i, s in enumerate(summaries, 1):
        print(f"Summary {i}:\n{s}\n")

    print("\nSynthesis:\n", synthesis)
