from typing import List, Dict
from pathlib import Path
import google.generativeai as genai
import sys
sys.path.append(str(Path(__file__).resolve().parents[1])) 

# Load your Google Gemini API key from environment or config file
from app.config import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

# Load custom prompt template
PROMPT_PATH = Path(__file__).resolve().parents[1] / 'prompts' / 'summarize_prompt.txt'
SUMMARIZE_PROMPT_TEMPLATE = PROMPT_PATH.read_text()

def summarize_paper(paper: Dict) -> str:
    """
    Uses Gemini to generate a concise summary of the paper.
    """
    content = f"Title: {paper['title']}\n\nAbstract: {paper['summary']}"
    prompt = SUMMARIZE_PROMPT_TEMPLATE.replace("{{content}}", content)

    model = genai.GenerativeModel("gemma-3-27b-it")
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    from agents.search_agent import search_arxiv
    papers = search_arxiv("aspect based sentiment analysis", max_results=1)
    summary = summarize_paper(papers[0])
    print("\nGenerated Summary:\n", summary)

# import google.generativeai as genai

# # Initialize API
# genai.configure(api_key="your api key")

# # List all available models
# models = genai.list_models()
# for model in models:
#     print(model.name)
