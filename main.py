from groq import Groq
from dotenv import load_dotenv
import os

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

def banner_is():
    print("hiikkkking")
    return "Banner is finished"
def firendly_reminder():
    print("Don't forget to take your umbrella out")
tools = [
    {
        "type": "function",
        "function": {
            "name": "banner_is",
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
            "name": "firendly_reminder",
            "description": "Prints a test message.",
            "parameters": {
                "type": "object",
                "properties": {}
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
    new_response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=input_msg,
        tools=tools
    )
    reply = new_response.choices[0].message
    
    print(f"message len {len(input_msg)}")
    if len(input_msg) > 12:
        print(f"exceed the limit now {len(input_msg)}")
        input_msg = input_msg[-12:]
    array_1 = [0, 1, 2, 3, 4]
    array_1.append(3)
    print(array_1)
    if reply.tool_calls:
        print("tool has been called")
        for tool in reply.tool_calls:
            if tool.function.name == "banner_is":
                banner_is()
            if tool.function.name == "firendly_reminder":
                firendly_reminder()
        print("__calling__")
        print(reply.content)
    else:
        input_msg.append({
            "role": "assistant",
            "content": reply.content
        })
        print(reply.content)