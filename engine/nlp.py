from transformers import pipeline

# We load the model once and reuse it
# (loading every time would be slow — ~5 seconds each)
_emotion_pipeline = None

def get_pipeline():
    global _emotion_pipeline
    if _emotion_pipeline is None:
        _emotion_pipeline = pipeline(
            "text-classification",
            model="bhadresh-savani/distilbert-base-uncased-emotion",
            top_k=None,
        )
    return _emotion_pipeline


def analyze_text(text):
    if not text or len(text.strip()) < 5:
        return None

    pipe = get_pipeline()
    raw = pipe(text[:512])[0]  # list of {label, score}

    # Convert to a simple dict: {"joy": 0.12, "sadness": 0.43, ...}
    emotions = {}
    for item in raw:
        emotions[item["label"].lower()] = round(item["score"], 4)

    # Find which emotion scored highest
    dominant = max(emotions, key=emotions.get)

    return {
        "emotions": emotions,
        "dominant": dominant,
    }

def compute_scores(emotions):
    """
    Takes the emotions dict and return two numbers:
    - health_bar: 0 (burnout) to 100 (flow)
    - efv_score: 0 (stuck) to 100 (hyperfocus)
    """
    joy      = emotions.get("joy", 0)
    sadness  = emotions.get("sadness", 0)
    fear     = emotions.get("fear", 0)
    anger    = emotions.get("anger", 0)
    surprise = emotions.get("surprise", 0)
    disgust  = emotions.get("disgust", 0)

     # Health bar: joy pushes it right, fear/sadness push it left
    health_bar = 50 + (joy * 40) - (fear * 35) - (sadness * 30) - (disgust * 15)
    health_bar = max(0, min(100, health_bar))

    # EFV: measures how "available" your executive function is
    efv = 50 + (joy * 30) - (fear * 25) - (sadness * 20) + (surprise * 10) - (anger * 10)
    efv = max(5, min(98, efv))

    return {
        "health_bar": round(health_bar, 1),
        "efv_score":  round(efv, 1),
    }