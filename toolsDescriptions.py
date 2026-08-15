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
    },
    {
        "type": "function",
        "function": {
            "name": "write_multiple_files",
            "description": """Write multiple files to disk.

                Each file contains:
                - file_path: the path of the file
                - content: the complete contents of the file

                Preserve the file content exactly, including newlines, quotes,
                backslashes, tabs, and other characters.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_infos": {
                        "type": "array",
                        "description": "All Files with its content that need to be written",
                        "items": {
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "The path of the file to write."
                                },
                                "content": {
                                    "type": "string",
                                    "description": "The content to write into the file."
                                }
                            },
                            "required": ["file_path", "content"],
                            "additionalProperties": False
                        }
                    } 
                },
                "required": ["file_infos"],
                "additionalProperties": False
            }
        }
    }
]