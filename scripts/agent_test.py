"""
Step 3 test: exercise the M6 agent core end-to-end.
Try a plain question and a tool-triggering question.
"""

import asyncio
import sys
sys.path.insert(0, ".")

from server.modules.agent.core import run
from server.modules.agent.history import ConversationHistory


async def ask(message: str) -> None:
    history = ConversationHistory()
    print(f"\nYou: {message}")
    print("Assistant: ", end="", flush=True)
    async for chunk in run(message, history):
        print(chunk, end="", flush=True)
    print()


async def main() -> None:
    await ask("What is the capital of Japan?")
    await ask("Search the web for the latest Python version.")
    await ask("Turn on my bedroom light.")


asyncio.run(main())
