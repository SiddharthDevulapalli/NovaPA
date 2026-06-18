# Personal AI Voice Assistant

A hybrid voice assistant built as a learning project. You speak a wake word, ask a question or give a command, and hear a spoken response.

> **Note:** This project was vibe coded with AI assistance (Claude Code by Anthropic). The architecture, implementation decisions, and all code were developed collaboratively through conversation.

---

## Architecture

The assistant runs as two separate components:

- **Hosted server** (FastAPI on Railway) — handles all AI: speech-to-text, LLM, RAG, TTS, web search
- **Local agent** (Python app on Mac) — handles OS-level actions: wake word detection, mic capture, smart lights, macOS reminders, browser/YouTube

The two components communicate exclusively through a WebSocket bridge.

---

## Features

| Feature | Status | Description |
|---|---|---|
| Wake word detection | ✅ | Say "hey jarvis" (or custom word) to activate |
| Voice activity detection | ✅ | Records until you stop speaking |
| Speech to text | ✅ | Transcribes your voice using Deepgram |
| AI responses | ✅ | Claude answers questions and executes commands |
| Text to speech | ✅ | Speaks responses aloud via ElevenLabs |
| Web search | ✅ | Searches the web via Brave Search API |
| Set reminders | ✅ | Creates reminders in macOS Reminders.app |
| Open browser | ✅ | Opens URLs in your default browser |
| Play YouTube | ✅ | Searches YouTube and plays the top result |
| RAG (document Q&A) | ✅ | Upload PDFs and ask questions about them |
| Smart light control | 🚧 | Kasa lights blocked by router AP isolation |
| React UI | 🚧 | Voice button, chat stream, latency dashboard |
| WebSocket bridge | 🚧 | Local ↔ hosted communication layer |
| Custom wake word | 🚧 | Train a custom "nova" wake word model |

---

## APIs & Libraries

| What it does | API / Library |
|---|---|
| LLM (reasoning + tool use) | [Anthropic Claude](https://anthropic.com) — `claude-sonnet-4-6` |
| Speech to text | [Deepgram](https://deepgram.com) — Nova-2 model |
| Text to speech | [ElevenLabs](https://elevenlabs.io) — `eleven_turbo_v2_5` |
| Web search | [Brave Search API](https://brave.com/search/api) — DIY implementation, no SDK |
| Vector database (RAG) | [ChromaDB](https://chromadb.com) — local persistent store |
| Embeddings (RAG) | [OpenAI](https://openai.com) — `text-embedding-3-small` |
| YouTube playback | [YouTube Data API v3](https://developers.google.com/youtube) |
| Wake word detection | [OpenWakeWord](https://github.com/dscripka/openWakeWord) — on-device |
| Smart lights | [python-kasa](https://github.com/python-kasa/python-kasa) — Kasa/TP-Link |
| Server framework | [FastAPI](https://fastapi.tiangolo.com) + uvicorn |
| Audio I/O | [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) |
| HTML parsing (web scraper) | [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io) + httpx |
| Data validation | [Pydantic](https://docs.pydantic.dev) |

---

## Project Structure

```
personal-assistant/
├── server/                  # Hosted on Railway
│   └── modules/
│       ├── agent/           # Claude agent core + tool dispatch
│       ├── stt/             # Deepgram speech-to-text
│       ├── tts/             # ElevenLabs text-to-speech
│       ├── web_search/      # Brave API web search + scraper
│       └── rag/             # ChromaDB RAG pipeline
│
├── agent/                   # Runs locally on Mac
│   ├── main.py              # Full voice loop entry point
│   └── modules/
│       ├── wake_word/       # OpenWakeWord detector
│       ├── vad/             # Voice activity detection
│       ├── lights/          # Kasa smart light control
│       ├── mac_actions/     # Reminders + notifications via AppleScript
│       └── browser/         # Browser opener + YouTube
│
├── scripts/                 # Standalone learning/test scripts
└── audio_files/             # Recorded audio (gitignored)
```

---

## Setup

```bash
# Clone and create virtual environment
git clone <repo-url>
cd personal-assistant
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install anthropic python-dotenv httpx beautifulsoup4 \
            chromadb openai PyPDF2 pyaudio openwakeword \
            pydantic python-kasa fastapi uvicorn

# Copy and fill in API keys
cp .env.example .env   # then edit .env with your keys

# Run the voice assistant
python agent/main.py
```

---

## Environment Variables

```
ANTHROPIC_API_KEY       # Claude LLM
DEEPGRAM_API_KEY        # Speech to text
ELEVENLABS_API_KEY      # Text to speech
ELEVENLABS_VOICE_ID     # ElevenLabs voice
BRAVE_SEARCH_API_KEY    # Web search
YOUTUBE_API_KEY         # YouTube playback
OPENAI_API_KEY          # RAG embeddings
WAKE_WORD_NAME          # Wake word name (default: nova)
WAKE_WORD_THRESHOLD     # Detection sensitivity 0-1 (default: 0.5)
TTS_STREAMING           # true = paid ElevenLabs plan, false = free
```

---

## Key Design Decisions

- **No LangChain** — all tool use, streaming, and agent loops are implemented from scratch for learning purposes
- **No built-in Claude tools** — web search, reminders, YouTube are all custom implementations
- **Loose coupling** — every module has a clean interface and knows nothing about other modules
- **Graceful degradation** — every external API call has a timeout and fallback
- **Local/hosted split** — local agent handles LAN + OS access, hosted server handles all AI
