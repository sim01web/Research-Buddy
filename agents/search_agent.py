import requests
from typing import List, Dict

def search_arxiv(query: str, max_results: int = 10) -> List[Dict]:
    """
    Searches arXiv for papers matching the query.
    Returns a list of dictionaries with paper metadata.
    """
    base_url = "http://export.arxiv.org/api/query?"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception("Error fetching data from arXiv API")

    from xml.etree import ElementTree as ET
    root = ET.fromstring(response.text)

    papers = []
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        paper = {
            "title": entry.findtext("{http://www.w3.org/2005/Atom}title"),
            "summary": entry.findtext("{http://www.w3.org/2005/Atom}summary"),
            "authors": [author.findtext("{http://www.w3.org/2005/Atom}name") for author in entry.findall("{http://www.w3.org/2005/Atom}author")],
            "link": entry.findtext("{http://www.w3.org/2005/Atom}id"),
            "published": entry.findtext("{http://www.w3.org/2005/Atom}published")
        }
        papers.append(paper)
    return papers

if __name__ == "__main__":
    results = search_arxiv("aspect based sentiment analysis")
    for i, paper in enumerate(results):
        print(f"\nPaper {i+1}: {paper['title']}\nPublished: {paper['published']}\nLink: {paper['link']}\n")