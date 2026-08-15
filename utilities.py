from typing import TypedDict, List
import os
from groq import Groq
from dotenv import load_dotenv
from enum import Enum

load_dotenv()
class FileInfo(TypedDict):
    file_path: str
    content: str
available_paths: List[str] = [
    "./"
    "/Users/venghour/Documents/Coding/Games/Office_gangstar"
]
class AIPlatformsType(Enum):
    Groq_T=1
    Ollama_T=2
messages = [
    {
        "role": "system",
        "content": """
        You are an AI assistant with access to tools.

        Available tools:
        - banner_is: checks banner status
        - friendly_reminder: gives a reminder message
        - read_file: return what contain inside the file
        - write_file: writing and replacing text into file
        - write_multiple_files: writing and replacing multiple files at once

        Rules:
        - Only call tools listed above.
        - Never invent new tools.
        - If a user asks about available tools, answer directly.
        """
    }
]
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
a: int = 2