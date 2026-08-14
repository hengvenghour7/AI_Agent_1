
from typing import List
from groq.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall
import json
import allTools
import utilities
from groq import Groq
import os
from toolsDescriptions import tools
import ollama

TOOLS_EXECUTE_TRIES_LIMIT = 10
AIPlatformsType = utilities.AIPlatformsType
def execute_AI_tool(tool_calls: List[ChatCompletionMessageToolCall]) -> None:
    for tool in tool_calls:
        function = allTools.available_tools[tool.function.name]
        args = tool.function.arguments
        result = function(**args)
        utilities.messages.append({
                    "role": "tool",
                    # "tool_call_id": tool.id,
                    "content": str(result)
                })
def create_AI_response(AIPlatform: AIPlatformsType):
    if AIPlatform == AIPlatformsType.Groq_T:
        response = utilities.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=utilities.messages,
            tools=tools
        )
    if AIPlatform == AIPlatformsType.Ollama_T:
        response = ollama.chat(
                    model="gpt-oss:20b",
                    messages=utilities.messages,
                    tools=tools
                )
    return response

def increase_a():
    utilities.a += 3