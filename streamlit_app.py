import streamlit as st
import cv2
import numpy as np
from keras.models import load_model
import wave
from vosk import Model, KaldiRecognizer
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load emotion model once
@st.cache_resource
def load_emotion_model():
    model_path = "model/fer2013_mini_XCEPTION.102-0.66.hdf5"
    return load_model(model_path, compile=False)

# Emotion Detection
def detect_emotion(image, model):
    emotion_dict = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}
    try:
        img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = cv2.resize(gray, (64, 64))
        face = np.reshape(face, (1, 64, 64, 1)) / 255.0
        prediction = model.predict(face)
        return emotion_dict[np.argmax(prediction)]
    except Exception as e:
        return f"Error: {e}"

# Voice Duration
def analyze_voice(audio_file):
    try:
        with wave.open(audio_file, 'rb') as wf:
            framerate = wf.getframerate()
            nframes = wf.getnframes()
            duration = nframes / float(framerate)
        return duration
    except Exception as e:
        return f"Error: {e}"

# Transcription
def transcribe_audio(audio_file):
    try:
        model_path = "model/vosk-model-small-en-us-0.15"
        model = Model(model_path)
        rec = KaldiRecognizer(model, 16000)
        rec.SetWords(True)

        wf = wave.open(audio_file, "rb")
        results = []

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                results.append(json.loads(rec.Result()))

        results.append(json.loads(rec.FinalResult()))
        transcript = " ".join([res.get("text", "") for res in results])
        return transcript
    except Exception as e:
        return f"Error: {e}"

# Keyword Extraction
def extract_keywords(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    keywords = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    return keywords

# ========================== STREAMLIT UI ==========================

st.set_page_config(page_title="AI Interview Evaluator", layout="centered")
st.title("🎤 AI-Powered Interview Evaluator")

st.markdown("Upload a photo (face) and voice recording to analyze:")

image_file = st.file_uploader("Upload Face Image", type=["jpg", "png", "jpeg"])
audio_file = st.file_uploader("Upload Voice (WAV format only)", type=["wav"])

if image_file and audio_file:
    st.success("Files uploaded! Starting evaluation...")

    model = load_emotion_model()
    emotion = detect_emotion(image_file, model)
    voice_duration = analyze_voice(audio_file)
    transcript = transcribe_audio(audio_file)
    keywords = extract_keywords(transcript)

    st.subheader("📊 Final Analysis")
    st.write(f"**Emotion Detected:** {emotion}")
    st.write(f"**Voice Duration:** {voice_duration:.2f} seconds" if isinstance(voice_duration, float) else voice_duration)
    st.write(f"**Transcript:** {transcript}")
    st.write(f"**Keywords:** {', '.join(keywords)}")

elif image_file or audio_file:
    st.warning("Please upload **both** face image and voice file to proceed.")

