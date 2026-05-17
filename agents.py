# agents.py

import arxiv
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------
# OPENROUTER
# -----------------------------------
def query_openrouter(prompt, model):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "OPENROUTER_API_KEY not found."

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:

        return f"Error: {str(e)}"

# -----------------------------------
# SEARCH PAPERS
# -----------------------------------
def academic_websearch_agent(topic):

    papers = []

    try:

        search = arxiv.Search(
            query=topic,
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )

        client = arxiv.Client()

        for result in client.results(search):

            papers.append({

                "title": result.title,

                "summary": result.summary,

                "authors": [a.name for a in result.authors],

                "published": str(result.published.date()),

                "url": result.entry_id
            })

    except Exception as e:

        print(e)

    return papers

# -----------------------------------
# ANALYSIS
# -----------------------------------
def academic_analysis_agent(topic, papers, model):

    if not papers:
        return "No papers found."

    text = ""

    for i, paper in enumerate(papers, start=1):

        text += f"""

Paper {i}

Title: {paper['title']}

Authors: {', '.join(paper['authors'])}

Published: {paper['published']}

Summary:
{paper['summary']}

"""

    prompt = f"""
You are an academic research analyst.

Topic:
{topic}

Analyze these papers and provide clearly separated sections:

1. Research Trends
2. Key Findings
3. Limitations
4. Future Scope
5. Applications
6. Conclusion
7. Simple Conclusion

IMPORTANT:
- Keep "Conclusion" and "Simple Conclusion" separate.
- Use proper headings.
- Simple Conclusion must be short and beginner friendly.

{text}
"""

    return query_openrouter(prompt, model)

# -----------------------------------
# COORDINATOR
# -----------------------------------
def academic_coordinator(topic, model):

    papers = academic_websearch_agent(topic)

    analysis = academic_analysis_agent(
        topic,
        papers,
        model
    )

    return papers, analysis
