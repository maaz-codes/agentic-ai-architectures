from langchain_tavily import TavilySearch


def get_profile_url_tavily(name: str):
    """Searches for Linkedin Profile Page."""

    search = TavilySearch()
    result = search.run(f"{name}")
    
    return result