from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
input_msg = [
    {
        "role": "system",
        "content": """
        You are an AI assistant with access to tools.

        Available tools:
        - banner_is: checks banner status
        - friendly_reminder: gives a reminder message
        _ read_file: return what contain inside the file

        Rules:
        - Only call tools listed above.
        - Never invent new tools.
        - If a user asks about available tools, answer directly.
        """
    }
]
# response = client.chat.completions.create(
#     model="llama-3.1-8b-instant",
#     messages = input_msg
# )

# print(response.choices[0].message.content)
def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()
def banner_is():
    print("hiikkkking")
    return "Banner is finished"
def friendly_reminder():
    print("Don't forget to take your umbrella out")
available_tools = {
    "read_file": read_file,
    "friendly_reminder": friendly_reminder,
    "banner_is": banner_is
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
                "description": "return what is inside the file",
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
        }
]
while True:
    user_input = input("User input: ")
    print("_______________________")
    input_msg.append({
        "role": "user",
        "content": user_input
    })
    try:
        new_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=input_msg,
            tools=tools
        )
    except Exception as e:
        print(f"Prompt error {e}")
        continue
    reply = new_response.choices[0].message
    
    print(f"message len {len(input_msg)}")
    if len(input_msg) > 12:
        print(f"exceed the limit now {len(input_msg)}")
        input_msg = input_msg[-12:]
    if reply.tool_calls:
        print("tool has been called")
        print(f"fadsf {reply.tool_calls}")
        res = ""
        try:
            for tool in reply.tool_calls:
                function = available_tools[tool.function.name]
                args = json.loads(tool.function.arguments)
                if args is None:
                    args = {}
                res = function(**args)
                # if res is not None:
                #     print(res)
                # print(final.choices[0].message.content)
                
        except Exception as e:
            print(f"error {e}")
        if res is not None:
            input_msg.append({
                                "role": "tool",
                                "tool_call_id": tool.id,
                                "content": res
                            })
        print("__calling__")
        try:
            final_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=input_msg,
                tools=tools
            )
            input_msg.append({
                        "role": "assistant",
                        "content": final_response.choices[0].message.content
                    })
            print(final_response.choices[0].message.content)
        except Exception as e:
            print(f"another error {e}")
    else:
        input_msg.append({
            "role": "assistant",
            "content": reply.content
        })
        print(reply.content)