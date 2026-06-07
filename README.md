# ◈ PSYCHE — Bio-Psychological Mirror

> A local, private biofeedback tool that reads your emotional state 
> and tells you what to do with your nervous system.

Built with Python + Streamlit. Runs 100% locally — no API keys, 
no subscriptions, no data leaving your machine.

---

## What it does

You write what's in your head. PSYCHE:
- Detects your emotional fingerprint using a local NLP model
- Translates it into neurochemical language (cortisol, dopamine, etc.)
- Shows your Executive Function Velocity on an analog gauge
- Prescribes a specific physical intervention to shift your state
- Speaks your diagnosis back to you via audio summary

---

## Stack

- **Streamlit** — UI framework
- **HuggingFace Transformers** — local emotion classification model
- **Plotly** — analog speedometer gauge
- **gTTS** — text-to-speech audio synthesis
- **BeautifulSoup4** — psychology content feed

---

## Run locally

```bash
git clone https://github.com/MounishPorandla/PSYCHE
cd PSYCHE
pip install -r requirements.txt
streamlit run app.py
```

The NLP model (~250MB) downloads automatically on first run.

---

## Architecture