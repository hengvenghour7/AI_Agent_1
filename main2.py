import json
from datetime import datetime
import ollama

# ===========================
# Python Tools
# ===========================

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def add(a: float, b: float):
    return a + b


available_tools = {
    "get_time": get_time,
    "add": add
}

# ===========================
# Tool Definitions
# ===========================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Return the current local date and time.",
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
                        "type": "number"
                    },
                    "b": {
                        "type": "number"
                    }
                },
                "required": ["a", "b"]
            }
        }
    }
]

messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant. Use tools whenever needed."
    }
]

print("===== Ollama AI Agent =====")
print("Type 'exit' to quit.\n")

while True:

    prompt = input("You: ")

    if prompt.lower() == "exit":
        break

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    while True:

        response = ollama.chat(
            model="llama3.2:3b",
            messages=messages,
            tools=tools
        )

        message = response["message"]

        # No tool calls
        if not message.get("tool_calls"):

            print("\nAssistant:", message["content"])
            print()

            messages.append(message)
            break

        messages.append(message)

        # Execute tool calls
        for tool in message["tool_calls"]:

            function_name = tool["function"]["name"]
            arguments = tool["function"].get("arguments", {})

            print(f"\nCalling Tool: {function_name}")
            print("Arguments:", arguments)

            result = available_tools[function_name](**arguments)

            print("Result:", result)

            messages.append(
                {
                    "role": "tool",
                    "name": function_name,
                    "content": str(result)
                }
            )