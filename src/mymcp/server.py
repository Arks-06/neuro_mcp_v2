import asyncio
from fastmcp import FastMCP
from tools.fs_io import read_file, write_file
from tools.memory import store_memory, recall_memory
from tools.websrch import web_search
from tools.emotion import analyze_emotion

# Initialize FastMCP Server
mcp = FastMCP(
    "Neuro_MCP_V2",
    # description="Advanced local capabilities server providing shared semantic memory, sandboxed I/O, web search, and emotional intelligence."
)

# File System Tools
@mcp.tool(name="read_workspace_file")
async def tool_read_file(file_path: str) -> str:
    """
    Read the full text contents from a specific file strictly inside the sandboxed workspace folder.
    Use this to get context from previous documents or code files.
    """
    return await read_file(file_path)

@mcp.tool(name="write_workspace_file")
async def tool_write_file(file_path: str, content: str) -> str:
    """
    Write or overwrite text content to a specific file inside the sandboxed workspace folder.
    Automatically creates directories if they do not exist. Use this to save notes, code, or outputs.
    """
    return await write_file(file_path, content)

# --- Shared Vector Memory Tools ---
@mcp.tool(name="store_persistent_memory")
def tool_store_memory(concept: str, details: str) -> str:
    """
    Store long-term semantic context or user preferences permanently in the vector database.
    Use this when the user explicitly asks you to remember something or when key insights are uncovered.
    """
    return store_memory(concept, details)

@mcp.tool(name="recall_persistent_memory")
def tool_recall_memory(query: str, n_results: int = 3) -> str:
    """
    Query the persistent vector database to recall past context, preferences, or project details.
    Use this to check if you have existing knowledge on a topic the user mentions.
    """
    return recall_memory(query, n_results)

# --- Live Web Search Tool ---
@mcp.tool(name="tavily_web_search")
async def tool_web_search(query: str) -> str:
    """
    Search the live web using the Tavily API for highly optimized real-time technical answers, 
    documentation, news, or updates.
    """
    return await web_search(query)

# --- Emotional Intelligence Tool ---
@mcp.tool(name="analyze_text_emotion")
def tool_analyze_emotion(text: str) -> str:
    """
    Locally run a deep learning classification pipeline to detect semantic emotional markers 
    (Joy, Sadness, Anger, Fear, Surprise, Disgust, Neutral) inside a block of text.
    Use this to adapt your tone or better understand user sentiment.
    """
    return analyze_emotion(text)

if __name__ == "__main__":
    # Runs the server using stdio transport layer for Claude Desktop connection
    mcp.run()