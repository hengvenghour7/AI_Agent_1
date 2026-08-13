
from typing import List
from groq.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall
import json
import toolHelpers
import utilities

TOOLS_EXECUTE_TRIES_LIMIT = 10
def execute_AI_tool(tool_calls: List[ChatCompletionMessageToolCall]) -> None:
    for tool in tool_calls:
        function = toolHelpers.available_tools[tool.function.name]
        args = json.loads(tool.function.arguments)
        result = function(**args)
        utilities.messages.append({
                    "role": "tool",
                    "tool_call_id": tool.id,
                    "content": str(result)
                })

def increase_a():
    utilities.a += 3