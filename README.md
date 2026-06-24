# Neuro MCP V2
## Description
Neuro MCP V2 is an advanced, production-grade local Model Context Protocol (MCP) server designed specifically for Claude Desktop. It supercharges Claude with a suite of agentic capabilities, bridging the gap between local execution and AI assistance using standard I/O (stdio) transport.

## Key Features
* **Persistent Semantic Memory:** Utilizes local embedded ChromaDB to store, embed, and instantly recall user context and project insights across different chat sessions.
* **Sandboxed File System I/O:** Safely reads and writes files asynchronously via `aiofiles` within a strict, path-traversal-protected `workspace/` directory.
* **Live Web Research:** Interacts with the Tavily Search API via `httpx` to pull real-time data, documentation, and news directly into Claude's context window.
* **Local Emotional Intelligence:** Runs a localized Hugging Face DistilRoBERTa pipeline via `transformers` and `torch` to analyze the semantic emotional tone of text blocks with zero external API latency.
* **Algorithmic Text Summarization:** Compresses long documents and web search dumps using an extractive summarization engine based on normalized word-frequency scoring, instantly extracting key informational sentences to prevent LLM context window exhaustion.
* **Zero-Dependency Entity & Intent Extraction:** Parses unstructured text records locally using a highly optimized, regex-based NLP engine to instantly extract critical parameters (IPs, emails, URLs, monetary bounds) and classify system operational intent.

## Architecture & Tech Stack
* **Framework:** `fastmcp` (Official Python SDK for MCP)
* **Package Management:** `uv` (Fast Python dependency resolution)
* **Database:** `chromadb` (Serverless, local SQLite vector storage)
* **Machine Learning:** `transformers`, `torch`
* **Async Operations:** `aiofiles`, `httpx`

## Project Structure
```markdown
neuro_mcp_v2/
├── .venv/
├── memory_db/             
├── workspace/     
├── .python-version
├── README.md
├── main.py
├── pyproject.toml
├── src/
    ├── mymcp/
        ├── server.py
        ├── tools/
            ├── emotion.py
            ├── fs_io.py
            ├── memory.py
            ├── websrch.py
            ├── extractor.py
            ├── summarize.py
        ├── utils/
            ├── security.py
├── uv.lock
```

## Prerequisites
* Python: 3.10 or higher
* Claude Desktop Application
* Tavily API Key: For web search capabilities

## Installation
Clone the repository and navigate to the project root.
Sync the dependencies using uv:
```bash
uv sync
```
Crucial Pre-flight Step: Run the server manually once to cache the Hugging Face emotion model (~300MB) locally and prevent Claude Desktop initialization timeouts:
```bash
uv run src/mymcp/server.py
```
Press Ctrl + C once the model finishes downloading.

## Claude Desktop Configuration
To connect this server to Claude, edit your Claude Desktop configuration file (located at %APPDATA%\Claude\claude_desktop_config.json on Windows).
[or simply go to Claude Desktop -> profile -> settings -> developer -> edit config option(if the mcp option is not shown automatically) -> make changes to the file that opens]
Point the command to your project's absolute path and supply your API keys in the environment block:
```json
{
  "mcpServers": {
    "neuro-mcp-v2": {
      "command": "C:\\Absolute\\Path\\To\\second_mcp_server\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Absolute\\Path\\To\\second_mcp_server\\src\\mymcp\\server.py"
      ],
      "env": {
        "PYTHONUTF8": "1",
        "TAVILY_API_KEY": "your_tavily_api_key_here"
      }
    }
  }
}
```
Restart Claude Desktop entirely after updating this file. You should see the MCP plug icon appear in your chat window.

## Security Notice
This application includes a workspace/ sandbox. The security middleware prevents the AI from reading or writing files outside of this specific directory to protect your local machine. Do not bypass the security.py checks.

## License
This project is licensed under the MIT License.