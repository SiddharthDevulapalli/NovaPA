"""
Step 1: Learn Claude streaming.
Sends a prompt and prints each token as it arrives, with timestamps.
"""

import os
import time
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

prompt = "Write a detailed story about an astronaut stranded on Mars who has to survive for 30 days using only what's in their ship."

print(f"Sending prompt: {prompt!r}\n")
print("-" * 40)

start = time.time()
first_token_time = None

with client.messages.stream(
    model="claude-haiku-4-5-20251001",
    max_tokens=256,
    messages=[{"role": "user", "content": prompt}],
) as stream:
    for token in stream.text_stream:
        now = time.time()
        if first_token_time is None:
            first_token_time = now
            print(f"[TTFB: {first_token_time - start:.3f}s]\n")
        print(token, end="", flush=True)

total = time.time() - start
print(f"\n\n[Total: {total:.3f}s | TTFB: {first_token_time - start:.3f}s]")
