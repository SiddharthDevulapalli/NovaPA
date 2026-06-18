import os
from dotenv import load_dotenv

load_dotenv()

WAKE_WORD_NAME = os.getenv("WAKE_WORD_NAME", "nova")
WAKE_WORD_THRESHOLD = float(os.getenv("WAKE_WORD_THRESHOLD", "0.7"))
WAKE_WORD_MODEL_PATH = os.getenv("WAKE_WORD_MODEL_PATH", "wake_word_model/custom.onnx")
PRETRAINED_MODEL = "hey_jarvis"
AUDIO_CHUNK = 1280
SAMPLE_RATE = 16000
