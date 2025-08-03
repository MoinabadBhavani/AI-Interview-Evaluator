# ai_interview_evaluator.py

from deepface import DeepFace
import cv2
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import wave
from vosk import Model, KaldiRecognizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

nltk.download('punkt')
nltk.download('stopwords')

def detect_emotion():
    cap = cv2.VideoCapture(0)
    print("📷 Detecting facial emotion. Press 'q' to capture...")

    while True:
        ret, frame = cap.read()
        cv2.imshow('Press q to capture emotion', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("face.jpg", frame)
            break

    cap.release()
    cv2.destroyAllWindows()

    result = DeepFace.analyze(img_path="face.jpg", actions=['emotion'], enforce_detection=False)
    emotion = result[0]['dominant_emotion']
    print(f"😊 Detected Emotion: {emotion}")
    return emotion

def record_voice():
    print("🎙️ Recording... Speak for 5 seconds.")
    fs = 44100
    duration = 5
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write("voice.wav", fs, recording)
    print("✅ Saved: voice.wav")

def analyze_frequency():
    import scipy.io.wavfile as wav
    from scipy.fft import fft

    rate, data = wav.read("voice.wav")
    data = data[:, 0] if len(data.shape) == 2 else data
    data = data[:rate]
    fft_out = fft(data)
    freqs = np.fft.fftfreq(len(fft_out))
    peak_freq = abs(freqs[np.argmax(np.abs(fft_out))] * rate)
    
    tone = "Neutral"
    if peak_freq < 300:
        tone = "Calm"
    elif 300 <= peak_freq < 600:
        tone = "Anxious"
    else:
        tone = "Aggressive"

    print(f"📊 Peak Frequency: {peak_freq:.2f} Hz")
    print(f"🧠 Voice Tone Analysis: {tone}")
    return tone

def transcribe_audio():
    print("🧠 Transcribing...")
    model_path = r"C:\Users\mb397\OneDrive\Desktop\model\vosk-model-small-en-us-0.15"
    if not os.path.exists(model_path):
        print("❌ Model path is incorrect.")
        return ""

    model = Model(model_path)
    wf = wave.open("voice.wav", "rb")

    if wf.getsampwidth() != 2 or wf.getnchannels() != 1 or wf.getframerate() != 44100:
        print("❌ Audio file format is not supported.")
        return ""

    rec = KaldiRecognizer(model, wf.getframerate())
    transcript = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            transcript += result

    final_result = rec.FinalResult()
    transcript += final_result
    import json
    try:
        text = json.loads(transcript)["text"]
    except:
        text = "Could not parse transcript"

    print(f"📜 Final Transcript: {text}")
    return text

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    keywords = [w for w in word_tokens if w.lower() not in stop_words]
    return keywords

def main():
    emotion = detect_emotion()
    record_voice()
    tone = analyze_frequency()
    transcript = transcribe_audio()
    if transcript:
        keywords = extract_keywords(transcript)
        print(f"🔑 Keywords Extracted: {keywords}")
    else:
        print("❌ No transcript to analyze.")

if __name__ == "__main__":
    main()
