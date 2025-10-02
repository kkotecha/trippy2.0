from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
import os

@tool
def web_search(query: str) -> str:
    """
    Search the web for current information using Tavily.

    Args:
        query: Search query string

    Returns:
        Formatted search results with titles and content

    Example:
        web_search("best time to visit Japan")
    """
    try:
        search = TavilySearchResults(
            max_results=5,
            api_key=os.getenv("TAVILY_API_KEY")
        )
        results = search.invoke(query)

        formatted = []
        for r in results:
            formatted.append(
                f"Title: {r.get('title', 'N/A')}\n"
                f"Content: {r.get('content', 'N/A')}\n"
                f"URL: {r.get('url', 'N/A')}"
            )

        return "\n\n---\n\n".join(formatted)
    except Exception as e:
        return f"Search failed: {str(e)}. Using LLM knowledge instead."
