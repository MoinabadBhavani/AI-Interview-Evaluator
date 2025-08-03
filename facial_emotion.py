import cv2
from deepface import DeepFace

# Emoji Dictionary for Emotions
emojis = {
    'angry': '😠',
    'disgust': '🤢',
    'fear': '😨',
    'happy': '😄',
    'sad': '😢',
    'surprise': '😲',
    'neutral': '😐'
}

def detect_emotion():
    cap = cv2.VideoCapture(0)
    print("📸 Starting camera... Press 'q' to capture and analyze emotion.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break
        cv2.imshow('Live Feed - Press q to capture', frame)
        
        # Press 'q' to capture and analyze
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("face.jpg", frame)
            print("📷 Image captured.")
            break

    cap.release()
    cv2.destroyAllWindows()

    try:
        # Analyze emotion
        result = DeepFace.analyze(img_path="face.jpg", actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        emoji = emojis.get(emotion, '')
        print(f"😊 Detected Emotion: {emotion.capitalize()} {emoji}")
    except Exception as e:
        print("❌ Emotion detection failed:", str(e))

if __name__ == "__main__":
    detect_emotion()
