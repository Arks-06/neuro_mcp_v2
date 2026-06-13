from pathlib import Path
import os

# from security.py -> utils -> mymcp -> src -> root -> workspace
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
WORKSPACE_DIR = BASE_DIR / "workspace"

def secure_path(requested_path: str) -> Path:
    """
    Resolves a path and ensures it stays within the workspace sandbox.
    Raises PermissionError if path traversal is detected.
    """
    # Ensure the workspace directory actually exists
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Resolve the requested path 
    target_path = (WORKSPACE_DIR / requested_path).resolve()
    
    # Check if the final resolved path still lives inside the workspace
    if not str(target_path).startswith(str(WORKSPACE_DIR.resolve())):
        raise PermissionError(f"Access denied: Cannot access files outside the workspace. Attempted to access: {requested_path}")
    
    return target_path