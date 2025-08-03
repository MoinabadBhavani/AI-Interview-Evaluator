import speech_recognition as sr

def transcribe_audio(file_path="voice.wav"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    try:
        print("🧠 Transcribing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "🤷 Could not understand audio."
    except sr.RequestError as e:
        return f"❌ API unavailable or unresponsive: {e}"

# 🔽 This runs only if you run speech_to_text.py directly
if __name__ == "__main__":
    result = transcribe_audio("voice.wav")
    print("📜 Final Transcript:", result)
