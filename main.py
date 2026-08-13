from typing import List

from groq import Groq
from dotenv import load_dotenv
import os
import json
from pathlib import Path
from groq.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall

load_dotenv()
CURRENT_DIR = Path.cwd().resolve()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
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

        Rules:
        - Only call tools listed above.
        - Never invent new tools.
        - If a user asks about available tools, answer directly.
        """
    }
]
# response = client.chat.completions.create(
#     model="openai/gpt-oss-20b",
#     messages = messages
# )

# print(response.choices[0].message.content)
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
def execute_AI_tool(tool_calls: List[ChatCompletionMessageToolCall]) -> None:
    for tool in tool_calls:
        function = available_tools[tool.function.name]
        args = json.loads(tool.function.arguments)
        result = function(**args)
        messages.append({
            "role": "tool",
            "tool_call_id": tool.id,
            "content": str(result)
        })




    # if not response.tool_calls:
    #     return
    
    # messages.append(response)
    # result = None
    # try:
    #     for tool in response.tool_calls:
    #         function = available_tools[tool.function.name]
    #         args = json.loads(tool.function.arguments)
    #         result = function(**args)
    #     if result is not None:
    #             messages.append({
    #                 "role": "tool",
    #                 "tool_call_id": tool.id,
    #                 "content": str(result)
    #             })
    #     second_response = client.chat.completions.create(
    #                     model="openai/gpt-oss-20b",
    #                     messages=messages,
    #                     tools=tools
    #                 )
    # except Exception as e:
    #     print(f"error {e}")
    # try:
    #     print(second_response)
    #     execute_AI_tool(second_response.choices[0].message)
    # except Exception as e:
    #     print(f"second error {e}")

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
while True:
    user_input = input("User input: ")
    print("_______________________")
    messages.append({
        "role": "user",
        "content": user_input
    })
    try:
        new_response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools
        )
    except Exception as e:
        print(f"Prompt error {e}")
        continue
    reply = new_response.choices[0].message

    assistant_message = {
        "role": "assistant",
        "content": reply.content,
    }

    if reply.tool_calls:
        assistant_message["tool_calls"] = [
            {
                "id": tool.id,
                "type": "function",
                "function": {
                    "name": tool.function.name,
                    "arguments": tool.function.arguments,
                },
            }
            for tool in reply.tool_calls
        ]

    messages.append(assistant_message)  

        
    if reply.tool_calls:
        execute_AI_tool(reply.tool_calls)

        # Ask the AI what to say after seeing the tool result
        try:
            second_response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                tools=tools
            )
        except Exception as e:
            print(f"Second request error: {e}")
            continue

        second_reply = second_response.choices[0].message

        # Preserve second assistant message too
        messages.append({
            "role": "assistant",
            "content": second_reply.content
        })

        print(second_reply.content)
    else:
        print(reply.content)

    
    # if len(messages) > 12:
    #     messages = messages[-12:]
    # execute_AI_tool(reply)
    # print(f"finalll response {final_response}")
    # final_reply = final_response.choices[0].message
    # messages.append(final_reply)
    # print(f"testing response {final_response.choices[0].message}")
    # if final_response.choices[0].message.content is None:
    #     print("message is None")
    # messages.append({
    #     "role": "assistant",
    #     "content": reply.content
    # })
    # print(reply.content)
