import json
from datetime import datetime
import chromadb
from pathlib import Path
import os

CURRENT_FILE = Path(__file__).resolve()

# (tools -> mymcp -> src -> second_mcp_server)
PROJECT_ROOT = CURRENT_FILE.parent.parent.parent.parent

# database path explicitly in project folder
DB_PATH = PROJECT_ROOT / "memory_db"

# bulletproof absolute path
chroma_client = chromadb.PersistentClient(path=str(DB_PATH))
collection = chroma_client.get_or_create_collection(name="claude_shared_memory")

def store_memory(concept: str, details: str) -> str:
    """Stores a new memory concept in the database."""
    try:
        doc_id = f"mem_{int(datetime.now().timestamp())}"
        collection.add(
            documents=[details],
            metadatas=[{"concept": concept, "timestamp": datetime.now().isoformat()}],
            ids=[doc_id]
        )
        return f"Successfully stored memory for concept: {concept}"
    except Exception as e:
        return f"Failed to store memory: {e}"

def recall_memory(query: str, n_results: int = 3) -> str:
    """Searches the database for relevant memories."""
    if collection.count() == 0:
        return "No memories stored yet."
    
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        if not results['documents'][0]:
            return "No relevant memories found."
            
        formatted_results = []
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            formatted_results.append(f"Concept: {meta['concept']}\nDetails: {doc}")
            
        return "\n\n---\n\n".join(formatted_results)
    except Exception as e:
        return f"Failed to recall memory: {e}"