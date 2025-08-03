import os
import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model
import soundfile as sf
import wave
import json
import time
from vosk import Model, KaldiRecognizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

print("🟢 Script started")

# =================== Emotion Detection ===================
def detect_emotion(image_path='face.jpg', model_path='model/fer2013_mini_XCEPTION.102-0.66.hdf5'):

    print("📷 Detecting emotion...")
    emotion_dict = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

    try:
        model = load_model(model_path, compile=False)
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return "Model Load Error"

    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = cv2.resize(gray, (64, 64))  # Fixed this line
        face = np.reshape(face, (1, 64, 64, 1)) / 255.0
        prediction = model.predict(face)
        emotion = emotion_dict[np.argmax(prediction)]
        print(f"😀 Facial Emotion: {emotion}")
        return emotion
    except Exception as e:
        print(f"❌ Error in emotion detection: {e}")
        return "Emotion Detection Failed"


# =================== Voice Analysis ===================
def analyze_voice(audio_path='voice.wav'):
    print("🔊 Analyzing voice...")
    try:
        with wave.open(audio_path, 'rb') as wf:
            framerate = wf.getframerate()
            nframes = wf.getnframes()
            duration = nframes / float(framerate)
        print(f"📏 Voice Duration: {duration:.2f} seconds")
        return duration
    except Exception as e:
        print(f"❌ Error in voice analysis: {e}")
        return 0

# =================== Transcription ===================
def transcribe_audio(model_path='model/vosk-model-small-en-us-0.15', audio_path='voice.wav'):
    print("🎙️ Transcribing...")
    try:
        model = Model(model_path)
        rec = KaldiRecognizer(model, 16000)
        rec.SetWords(True)

        wf = wave.open(audio_path, "rb")
        results = []

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                results.append(json.loads(rec.Result()))

        results.append(json.loads(rec.FinalResult()))
        transcript = " ".join([res.get("text", "") for res in results])
        print(f"📝 Transcript: {transcript}")
        return transcript
    except Exception as e:
        print(f"❌ Error in transcription: {e}")
        return ""

# =================== Keyword Extraction ===================
def extract_keywords(text):
    print("🧠 Extracting keywords...")
    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    keywords = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    print(f"📌 Keywords: {keywords}")
    return keywords

# =================== Main ===================
def main():
    print("🔥 Main function started")

    emotion = detect_emotion()
    voice_duration = analyze_voice()
    transcript = transcribe_audio()
    keywords = extract_keywords(transcript)

    print("\n🔍 Final Interview Analysis:")
    print(f"😀 Emotion: {emotion}")
    print(f"📏 Voice Duration: {voice_duration:.2f} sec")
    print(f"📝 Transcript: {transcript}")
    print(f"📌 Keywords: {keywords}")

if __name__ == "__main__":
    main()
