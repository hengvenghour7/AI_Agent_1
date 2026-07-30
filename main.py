from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
input_msg = []
# response = client.chat.completions.create(
#     model="llama-3.1-8b-instant",
#     messages = input_msg
# )

# print(response.choices[0].message.content)

def banner_is():
    print("hiikkkking")
    return "Banner is finished"
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
    input_msg.append({
        "role": "assistant",
        "content": reply.content
    })
    print(f"message len {len(input_msg)}")
    if len(input_msg) > 12:
        print(f"exceed the limit now {len(input_msg)}")
        input_msg = input_msg[-12:]
    array_1 = [0, 1, 2, 3, 4]
    array_1.append(3)
    print(array_1)
    if reply.tool_calls:
        print("tool has been called");
    else:
        print(reply.content)