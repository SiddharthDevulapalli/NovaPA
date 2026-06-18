"""
Step 10: Learn PyAudio basics.
Records 5 seconds from mic, saves as WAV, plays it back.
"""

import wave
import pyaudio

RATE = 16000
CHUNK = 1024
CHANNELS = 1
FORMAT = pyaudio.paInt16
DURATION = 5
OUTPUT_FILE = "audio_files/test_recording.wav"

pa = pyaudio.PyAudio()

print("Recording for 5 seconds... speak now!")
stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

frames = []
for _ in range(int(RATE / CHUNK * DURATION)):
    frames.append(stream.read(CHUNK))

stream.stop_stream()
stream.close()
print("Done recording.")

with wave.open(OUTPUT_FILE, "wb") as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
print(f"Saved to {OUTPUT_FILE}")

print("Playing back...")
stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
with wave.open(OUTPUT_FILE, "rb") as wf:
    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()
pa.terminate()
print("Playback done.")
