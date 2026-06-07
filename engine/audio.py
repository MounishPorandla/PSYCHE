import tempfile
import os

def synthesize(bio, dominant_emotion):
    script = (
        f"PSYCHE Daily Summary. "
        f"Dominant emotional signal: {dominant_emotion}. "
        f"Neurochemical state: {bio['label']}. "
        f"{bio['detail']} "
        f"Your somatic protocol: {bio['short']} "
        f"Execute the protocol. Then return to work."
    )

    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp_path = tmp.name
    tmp.close()

    try:
        from gtts import gTTS
        tts = gTTS(text=script, lang="en", slow=False)
        tts.save(tmp_path)

        with open(tmp_path, "rb") as f:
            return f.read()

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)