"""
Step 2: Learn Claude tool use.
Claude calls a fake get_weather tool, we return a result, Claude responds.
"""

import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

TOOLS = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name."}
            },
            "required": ["city"],
        },
    }
]

def fake_get_weather(city: str) -> str:
    return json.dumps({"city": city, "temp_c": 22, "condition": "sunny"})

messages = [{"role": "user", "content": "What's the weather like in Tokyo?"}]

# Round 1: Claude decides to call the tool
response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    tools=TOOLS,
    messages=messages,
)

print(f"Stop reason: {response.stop_reason}")
tool_use = next(b for b in response.content if b.type == "tool_use")
print(f"Tool called: {tool_use.name}  Args: {tool_use.input}")

result = fake_get_weather(**tool_use.input)
print(f"Tool result: {result}\n")

# Round 2: send tool result back, get final answer
messages += [
    {"role": "assistant", "content": response.content},
    {"role": "user", "content": [{"type": "tool_result", "tool_use_id": tool_use.id, "content": result}]},
]

final = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    tools=TOOLS,
    messages=messages,
)

print("Final response:")
print(final.content[0].text)
