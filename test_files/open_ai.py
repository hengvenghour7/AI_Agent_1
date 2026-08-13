import os
import json
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI

# ==========================
# Load API Key
# ==========================

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ==========================
# Python Functions (Tools)
# ==========================

def get_time():
    """Return current time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def add(a: float, b: float):
    """Add two numbers."""
    return a + b


# Dictionary mapping tool names to functions
available_tools = {
    "get_time": get_time,
    "add": add
}

# ==========================
# Tool Definitions
# ==========================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current local date and time.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"]
            }
        }
    }
]

# ==========================
# Conversation Memory
# ==========================

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful AI assistant. "
            "Use tools whenever they help answer the user's question."
        )
    }
]

print("=== OpenAI Python Agent ===")
print("Type 'exit' to quit.\n")

# ==========================
# Agent Loop
# ==========================

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    while True:

        response = client.chat.completions.create(
            model="gpt-5",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # No tool call -> print answer
        if not message.tool_calls:

            print("\nAssistant:", message.content)
            print()

            messages.append(
                {
                    "role": "assistant",
                    "content": message.content
                }
            )

            break

        # Store assistant message with tool calls
        messages.append(message)

        # Execute every requested tool
        for tool_call in message.tool_calls:

            function_name = tool_call.function.name

            arguments = json.loads(tool_call.function.arguments)

            print(f"\n🔧 Calling: {function_name}")
            print("Arguments:", arguments)

            result = available_tools[function_name](**arguments)

            print("Result:", result)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )