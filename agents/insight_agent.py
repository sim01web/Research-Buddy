# agents/insight_agent.py (Gemini Version)
from pathlib import Path
import google.generativeai as genai
import sys
sys.path.append(str(Path(__file__).resolve().parents[1])) 
# Load Gemini API key
from app.config import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

# Load prompt
PROMPT_PATH = Path(__file__).resolve().parents[1] / 'prompts' / 'insight_prompt.txt'
INSIGHT_PROMPT_TEMPLATE = PROMPT_PATH.read_text()

def generate_insights(synthesis: str) -> str:
    """
    Uses Gemini to generate novel research directions from synthesized content.
    """
    prompt = INSIGHT_PROMPT_TEMPLATE.replace("{{synthesis}}", synthesis)
    model = genai.GenerativeModel("gemma-3-27b-it")
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    from agents.synthesis_agent import synthesize_insights
    from agents.summarize_agent import summarize_paper
    from agents.search_agent import search_arxiv

    papers = search_arxiv("aspect based sentiment analysis", max_results=3)
    summaries = [summarize_paper(paper) for paper in papers]
    synthesis = synthesize_insights(summaries)
    insights = generate_insights(synthesis)

    print("\nSynthesis:\n", synthesis)
    print("\nSuggested Research Directions:\n", insights)
