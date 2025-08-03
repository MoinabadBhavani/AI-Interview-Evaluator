from vosk import Model, KaldiRecognizer
import wave
import json

wf = wave.open("voice.wav", "rb")

if wf.getsampwidth() != 2 or wf.getnchannels() != 1 or wf.getframerate() != 16000:
    print("❌ voice.wav must be WAV format PCM 16bit mono at 16kHz")
    exit(1)

model = Model(r"C:\Users\mb397\OneDrive\Desktop\model\vosk-model-small-en-us-0.15")



rec = KaldiRecognizer(model, wf.getframerate())

print("🧠 Transcribing...")
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        print("📝 Partial Transcript:", result["text"])

# Final result
final_result = json.loads(rec.FinalResult())
print("✅ Final Transcript:", final_result["text"])


