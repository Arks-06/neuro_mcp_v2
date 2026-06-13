import chromadb
import uuid
from pathlib import Path

# database path at the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DB_DIR = BASE_DIR / "memory_db"

# ChromaDB client (it will create the folder if it doesn't exist)
client = chromadb.PersistentClient(path=str(DB_DIR))

# a specific collection for Claude
memory_collection = client.get_or_create_collection(name="claude_shared_memory")

def store_memory(concept: str, details: str) -> str:
    """Store a persistent memory into the vector database."""
    try:
        doc_id = str(uuid.uuid4())
        
        memory_collection.add(
            documents=[details],
            metadatas=[{"concept": concept}],
            ids=[doc_id]
        )
        return f"Success: Memory regarding '{concept}' stored permanently."
    except Exception as e:
        return f"Error storing memory: {str(e)}"

def recall_memory(query: str, n_results: int = 3) -> str:
    """Search the vector database for relevant past memories."""
    try:
        results = memory_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        
        if not documents:
            return "No relevant memories found."
            
        output = "Recalled Memories:\n"
        for doc, meta in zip(documents, metadatas):
            output += f"- [{meta.get('concept', 'Unknown')}]: {doc}\n"
            
        return output
    except Exception as e:
        return f"Error recalling memory: {str(e)}"