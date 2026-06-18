import re
from typing import AsyncGenerator


async def stream_sentences(token_gen: AsyncGenerator[str, None]) -> AsyncGenerator[str, None]:
    buffer = ""
    async for token in token_gen:
        buffer += token
        while True:
            match = re.search(r"[.?!]\s+", buffer)
            if not match:
                break
            sentence = buffer[:match.end()].strip()
            buffer = buffer[match.end():]
            if sentence:
                yield sentence

    if buffer.strip():
        yield buffer.strip()
