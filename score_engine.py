# score_engine.py

def calculate_score(sentiment, emotion=None, pitch=None):
    score = (sentiment + 1) * 5  # Base score from sentiment

    # Optional: tweak score using emotion
    if emotion == "happy":
        score += 1
    elif emotion == "angry" or emotion == "sad":
        score -= 1

    # Optional: use pitch (high pitch = nervous?)
    if pitch and pitch > 300:
        score -= 0.5
    elif pitch and pitch < 100:
        score -= 0.5

    # Clamp between 0–10
    score = max(0, min(10, round(score, 2)))
    return score
