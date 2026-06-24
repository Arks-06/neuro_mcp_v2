import asyncio
import json
from fastmcp import FastMCP
from tools.fs_io import read_file, write_file
from tools.memory import store_memory, recall_memory
from tools.websrch import web_search
from tools.emotion import analyze_emotion
from tools.summarize import summarize_text
from tools.extractor import extract_entities_and_intent

mcp = FastMCP(
    "Neuro_MCP_V2",
    # description="Advanced local capabilities server providing shared semantic memory, sandboxed I/O, web search, and emotional intelligence."
)

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

@mcp.tool(name="tavily_web_search")
async def tool_web_search(query: str) -> str:
    """
    Search the live web using the Tavily API for highly optimized real-time technical answers, 
    documentation, news, or updates.
    """
    return await web_search(query)

@mcp.tool(name="analyze_text_emotion")
def tool_analyze_emotion(text: str) -> str:
    """
    Locally run a deep learning classification pipeline to detect semantic emotional markers 
    (Joy, Sadness, Anger, Fear, Surprise, Disgust, Neutral) inside a block of text.
    Use this to adapt your tone or better understand user sentiment.
    """
    return analyze_emotion(text)

@mcp.tool(name="summarize_document")
def tool_summarize_text(text: str, compression_ratio: float = 0.3, max_sentences: int = 5) -> str:
    """
    Analyze and extract the most significant, informational sentences from a long block of text,
    article, file content, or search dump. 
    Use this to instantly compress data when a user asks for a summary or before saving text to logs.
    """
    return summarize_text(text, ratio=compression_ratio, max_sentences=max_sentences)

@mcp.tool(name="extract_entities_and_intent")
def tool_extract_nlp(text: str) -> str:
    """
    Parses unstructured text records, web dumps, or prompt messages to extract critical parameters
    like emails, URLs, monetary bounds, IP addresses, and custom proper nouns. It simultaneously
    classifies the system operational intent behind the text.
    """
    result_dict = extract_entities_and_intent(text)
    return json.dumps(result_dict, indent=2)

# @mcp.tool(name="index_workspace")
# def tool_index_workspace() -> str:
#     """
#     Scans all text documents in the sandboxed workspace and indexes them into the 
#     semantic vector database. Run this when new files are added to the workspace 
#     so they become searchable.
#     """
#     return index_workspace_documents()

# @mcp.tool(name="search_workspace")
# def tool_search_workspace(query: str, n_results: int = 3) -> str:
#     """
#     Perform a deep semantic meaning-based search across all indexed workspace files.
#     Use this to find specific concepts, ideas, or data inside the user's local documents.
#     """
#     return search_workspace(query, n_results)

if __name__ == "__main__":
    # Runs the server using stdio transport layer for Claude Desktop connection
    mcp.run()