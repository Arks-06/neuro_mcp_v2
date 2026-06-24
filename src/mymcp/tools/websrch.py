import os
import httpx

_http_client = httpx.AsyncClient(timeout=15.0)

async def web_search(query: str) -> str:
    """Search the web using the Tavily API for real-time information."""
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY environment variable not set in Claude config."
    
    try:
        response = await _http_client.post(
            "https://api.tavily.com/search",
            json={
                "api_key": api_key, 
                "query": query, 
                "search_depth": "basic",
                "max_results": 3
            }
        )
        response.raise_for_status()
        data = response.json()
            
        results = data.get("results", [])
        if not results:
            return "No results found for the given query."
                
        formatted_output = "Search Results:\n\n"
        for res in results:
            formatted_output += f"Title: {res.get('title', 'No Title')}\n"
            formatted_output += f"URL: {res.get('url', 'No URL')}\n"
            formatted_output += f"Content: {res.get('content', '')}\n\n"
                
        return formatted_output.strip()
            
    except Exception as e:
        return f"Error performing web search: {str(e)}"