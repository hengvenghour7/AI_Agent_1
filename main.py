from typing import List, TypedDict

from groq import Groq
from dotenv import load_dotenv
import os
import json
from pathlib import Path
from groq.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall
from utilities import messages, AIPlatformsType
import allTools
from toolsDescriptions import tools
from helpers import (execute_AI_tool, TOOLS_EXECUTE_TRIES_LIMIT, increase_a, 
create_AI_response, get_AI_message)
from allTools import append_file

load_dotenv()
CURRENT_DIR = Path.cwd().resolve()

AI_choice: AIPlatformsType = AIPlatformsType.Ollama_T

while True:
    print("_______________________\n")
    user_input = input("User input: ")
    print("_______________________")
    messages.append({
        "role": "user",
        "content": user_input
    })
    try:
        new_response = create_AI_response(AI_choice)
    except Exception as e:
        print(f"Prompt error {e}")
        continue
    reply = get_AI_message(AI_choice, new_response)

    assistant_message = {
        "role": "assistant",
        "content": reply.content,
    }

    if reply.tool_calls:
        assistant_message["tool_calls"] = [
            {
                # "id": tool.id,
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
            second_response = create_AI_response(AI_choice)
            print(f"tool call attempt {index}")
        except Exception as e:
            print(f"Second request error: {e}")
            continue
        index += 1

        second_reply = get_AI_message(AI_choice, second_response)
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
