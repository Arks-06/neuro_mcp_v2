import aiofiles
from utils.security import secure_path

async def read_file(file_path: str) -> str:
    """Read contents from a file strictly inside the workspace sandbox."""
    try:
        safe_path = secure_path(file_path)
        if not safe_path.exists():
            return f"Error: File '{file_path}' does not exist."
        if not safe_path.is_file():
            return f"Error: '{file_path}' is not a file, it might be a directory."
            
        async with aiofiles.open(safe_path, mode='r', encoding='utf-8') as f:
            content = await f.read()
        return content
    except PermissionError as e:
        return str(e)
    except Exception as e:
        return f"Error reading file: {str(e)}"

async def write_file(file_path: str, content: str) -> str:
    """Write content to a file strictly inside the workspace sandbox."""
    try:
        safe_path = secure_path(file_path)
        # Automatically create any missing subfolders inside the workspace
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(safe_path, mode='w', encoding='utf-8') as f:
            await f.write(content)
        return f"Success: Successfully wrote to '{file_path}'."
    except PermissionError as e:
        return str(e)
    except Exception as e:
        return f"Error writing file: {str(e)}"