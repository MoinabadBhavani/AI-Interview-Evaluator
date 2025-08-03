from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
import string

# Download NLTK data (only first time)
nltk.download('punkt')
nltk.download('stopwords')

# Example: Replace with actual text from your speech_to_text.py
transcript = input("📝 Paste your transcribed text: ")

# Sentiment Analysis
blob = TextBlob(transcript)
sentiment = blob.sentiment.polarity  # -1 to 1

# Sentiment Label
if sentiment > 0.2:
    label = "Positive 😊"
elif sentiment < -0.2:
    label = "Negative 😟"
else:
    label = "Neutral 😐"

# Extract Keywords (remove stopwords and punctuation)
words = blob.words
filtered_words = [word.lower() for word in words if word.lower() not in stopwords.words('english') and word not in string.punctuation]

keywords = list(set(filtered_words))

# Interview-like scoring (very basic logic)
score = round((sentiment + 1) * 5, 2)  # Scale -1 to 1 into 0–10

# Results
print("\n📊 NLP Analysis Report")
print("-------------------------")
print(f"Sentiment Score: {sentiment:.2f}")
print(f"Sentiment Label: {label}")
print(f"Interview Score (0–10): {score}")
print(f"🧠 Keywords: {', '.join(keywords)}")
from score_engine import calculate_score

score = calculate_score(sentiment, emotion="neutral", pitch=180)
