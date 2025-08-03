import cv2

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
    print("✅ Image captured and saved as face.jpg")

def main():
    print("Starting AI Interview Evaluator...")
    detect_emotion()

if __name__ == "__main__":
    main()
