import os
import logging
from typing import AsyncGenerator

import anthropic
from dotenv import load_dotenv

from .tool_schemas import TOOLS
from .tool_dispatcher import dispatch
from .history import ConversationHistory

load_dotenv()
logger = logging.getLogger(__name__)

_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = os.getenv("AGENT_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = 1024
SYSTEM_PROMPT = "You are a helpful personal voice assistant. Be concise — your responses will be spoken aloud."


async def run(message: str, history: ConversationHistory) -> AsyncGenerator[str, None]:
    history.add_user(message)

    while True:
        response = _client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=history.get(),
        )

        if response.stop_reason == "tool_use":
            history.add_assistant(response.content)
            for block in response.content:
                if block.type == "tool_use":
                    logger.info("Tool call: %s args=%s", block.name, block.input)
                    result = await dispatch(block.name, block.input)
                    logger.info("Tool result: %s", result)
                    history.add_tool_result(block.id, result)

        elif response.stop_reason == "end_turn":
            text = next((b.text for b in response.content if hasattr(b, "text")), "")
            history.add_assistant(response.content)
            yield text
            break

        else:
            logger.warning("Unexpected stop_reason: %s", response.stop_reason)
            break
