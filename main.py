from typing import List, TypedDict

from groq import Groq
from dotenv import load_dotenv
import os
import json
from pathlib import Path
from groq.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall
from utilities import messages
import allTools
from toolsDescriptions import tools
from helpers import execute_AI_tool, TOOLS_EXECUTE_TRIES_LIMIT, increase_a

load_dotenv()
CURRENT_DIR = Path.cwd().resolve()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



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

    index:int = 1
    for _ in range(TOOLS_EXECUTE_TRIES_LIMIT):
        if not reply.tool_calls:
            break

        result = execute_AI_tool(reply.tool_calls)
    
        # Ask the AI what to say after seeing the tool result
        try:
            second_response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=messages,
                tools=allTools
            )
            print(f"tool call attempt {index}")
        except Exception as e:
            print(f"Second request error: {e}")
            continue
        index += 1

        second_reply = second_response.choices[0].message
        # Preserve second assistant message too
        reply = second_reply
        messages.append({
            "role": "assistant",
            "content": second_reply.content
        })

        print(second_reply.content)

    print(reply.content)

    
    # if len(messages) > 12:
    #     messages = messages[-12:]
