from langchain.tools import tool
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup


@tool
def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo and return relevant
    titles, URLs and snippets.
    """

    try:
        results = DDGS().text(
            query,
            max_results=3,
        )

        if not results:
            return "No search results found."

        output = []

        for result in results:
            title = result.get("title", "No title")
            url = result.get("href", "")
            snippet = result.get("body", "")

            output.append(
                f"Title: {title}\n" f"URL: {url}\n" f"Snippet: {snippet[:500]}"
            )

        return "\n\n---\n\n".join(output)

    except Exception as e:
        return f"Web search failed: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """
    Visit a URL and extract clean readable text
    using BeautifulSoup.
    """

    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary elements
        for tag in soup(
            ["script", "style", "nav", "footer", "header", "aside", "form"]
        ):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        # Clean excessive spaces
        text = " ".join(text.split())

        if not text:
            return "No readable content found on this page."

        # Limit content passed to the LLM
        return text[:8000]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
