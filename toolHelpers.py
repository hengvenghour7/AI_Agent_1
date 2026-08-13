from pathlib import Path

CURRENT_DIR = Path.cwd().resolve()

def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()
def write_file(file_path, content):
    requested_path = (CURRENT_DIR / file_path).resolve()

    if CURRENT_DIR not in requested_path.parents and requested_path != CURRENT_DIR:
        raise PermissionError("Cannot write outside the current directory.")
    with open(file_path, "w") as f:
        f.write(content)
    print("text has been replaceddd")
def banner_is():
    print("hiikkkking")
    return "Banner is finished"
def friendly_reminder():
    print("Don't forget to take your umbrella out")

available_tools = {
    "read_file": read_file,
    "friendly_reminder": friendly_reminder,
    "banner_is": banner_is,
    "write_file": write_file
}
tools = [
    {
        "type": "function",
        "function": {
            "name": "banner_is",
            "description": "This tool take no argument",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "friendly_reminder",
            "description": "Prints a test message.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": """return what is inside the file
                    IMPORTANT:
                        - Preserve the user's file path exactly.
                        - Do NOT convert relative paths into absolute paths.
                        - If the user gives ./main2.py, pass ./main2.py exactly.
                        - Do NOT invent or assume /home/user or any other directory.
                    """,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file to read."
                        }
                    },
                    "required": ["file_path"],
                    "additionalProperties": False
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "replacing text inside the file with new content provided",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file to write."
                        },
                        "content": {
                            "type": "string",
                            "description": "new text to write into file."
                        },
                    },
                    "required": ["file_path", "content"],
                    "additionalProperties": False
                }
            }
        }
]