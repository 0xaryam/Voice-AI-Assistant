import os
import asyncio

import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import cohere
import edge_tts
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

VOICE = "en-US-AriaNeural"

os.makedirs("audio", exist_ok=True)

#voice record
fs = 44100
seconds = 5

print("🎤 Speak now...")

recording = sd.rec(
    int(seconds * fs),
    samplerate=fs,
    channels=1,
    dtype="int16"
)

sd.wait()

audio_path = "audio/input.wav"
write(audio_path, fs, recording)

print("✅ Audio saved.")

# Whisper
print("⏳ Loading Whisper model...")
model = whisper.load_model("base")

result = model.transcribe(audio_path)

user_text = result["text"].strip()

print("\n📝 Recognized Text:")
print(user_text)

if not user_text:
    print("❌ No speech detected.")
    exit()

# Cohere
response = co.chat(message=user_text)

reply = response.text

print("\n🤖 AI Response:")
print(reply)

# Text To Speech
async def text_to_speech(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save("audio/output.mp3")

try:
    print("⏳ Generating speech...")
    asyncio.run(text_to_speech(reply))
    print("✅ Speech generation finished.")

except Exception as e:
    print("❌ TTS ERROR:")
    print(e)