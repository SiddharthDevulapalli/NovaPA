import pyaudio
from .config import AUDIO_CHUNK, SAMPLE_RATE


def open_stream() -> tuple[pyaudio.PyAudio, pyaudio.Stream]:
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=SAMPLE_RATE,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=AUDIO_CHUNK,
    )
    return pa, stream


def close_stream(pa: pyaudio.PyAudio, stream: pyaudio.Stream) -> None:
    stream.stop_stream()
    stream.close()
    pa.terminate()
