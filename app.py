import streamlit as st
import plotly.graph_objects as go
from engine.nlp import analyze_text, compute_scores
from engine.bio_engine import compute_bio_state
from engine.scraper import get_feed
from engine.audio import synthesize

st.set_page_config(
    page_title="PSYCHE",
    page_icon="🧬",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Share+Tech+Mono&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #040608 !important;
    color: #e8f4f8;
}
textarea {
    background: #0a0f14 !important;
    border: 1px solid #1a2535 !important;
    color: #e8f4f8 !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stButton > button {
    background: transparent !important;
    border: 1px solid #00ffe1 !important;
    color: #00ffe1 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
}
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem;">
    <div style="font-family:'Orbitron',monospace; font-size:3rem; font-weight:900;
                color:#00ffe1; letter-spacing:0.3em;
                text-shadow: 0 0 30px rgba(0,255,225,0.6);">
        ◈ PSYCHE ◈
    </div>
    <div style="font-family:'Share Tech Mono',monospace; font-size:0.75rem;
                color:#4a6278; letter-spacing:0.25em; margin-top:0.5rem;">
        BIO-PSYCHOLOGICAL MIRROR // LOCAL INSTANCE // PRIVATE
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Store results in session state so columns can both access them ──
if "result" not in st.session_state:
    st.session_state.result = None

# ════════════════════════════════════════
# TWO COLUMN LAYOUT
# ════════════════════════════════════════
left, right = st.columns([1.6, 1], gap="large")

# ════════════════════════════════════════
# LEFT COLUMN
# ════════════════════════════════════════
with left:

    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace; font-size:0.82rem;
                color:#7ecfca; margin-bottom:0.5rem;">
        ALCHEMICAL PROMPT:<br>
        <span style="color:#4a6278;">
            What is the loudest thought in your head right now?
            What are you avoiding today?
        </span>
    </div>
    """, unsafe_allow_html=True)

    journal_input = st.text_area(
        label="",
        placeholder="Begin transmission...",
        height=150,
        label_visibility="collapsed",
    )

    analyze_btn = st.button("⚡ ANALYZE")

    if analyze_btn:
        if not journal_input.strip():
            st.warning("Write something first.")
        else:
            with st.spinner("PARSING NEURAL SIGNAL..."):
                result = analyze_text(journal_input)
                result["scores"] = compute_scores(result["emotions"])
                result["bio"]    = compute_bio_state(result["emotions"])
                result["feed"]   = get_feed(result["dominant"])
                st.session_state.result = result

    # ── Only render visuals if we have a result ──
    if st.session_state.result:
        r          = st.session_state.result
        emotions   = r["emotions"]
        dominant   = r["dominant"]
        health_bar = r["scores"]["health_bar"]
        efv_score  = r["scores"]["efv_score"]
        bio        = r["bio"]

        # Pick bar color
        if health_bar < 35:
            bar_color  = "#ff2d55"
            glow_color = "rgba(255,45,85,0.5)"
        elif health_bar < 65:
            bar_color  = "#ffd700"
            glow_color = "rgba(255,215,0,0.4)"
        else:
            bar_color  = "#39ff14"
            glow_color = "rgba(57,255,20,0.5)"

        # ── Health Bar ──
        st.markdown(f"""
        <div style="margin: 1.5rem 0 1rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
                <span style="font-family:'Share Tech Mono',monospace; font-size:0.65rem;
                             color:#ff2d55; letter-spacing:0.1em;">
                    ◀ BURNOUT / CORTISOL FREEZE
                </span>
                <span style="font-family:'Orbitron',monospace; font-size:0.75rem;
                             color:{bar_color}; text-shadow: 0 0 10px {glow_color};">
                    {health_bar:.0f}%
                </span>
                <span style="font-family:'Share Tech Mono',monospace; font-size:0.65rem;
                             color:#39ff14; letter-spacing:0.1em;">
                    MOMENTUM / DOPAMINE FLOW ▶
                </span>
            </div>
            <div style="position:relative; height:20px; background:#0d1117;
                        border:1px solid #1a2535; border-radius:2px; overflow:hidden;">
                <div style="height:100%; width:{health_bar}%;
                            background: linear-gradient(90deg, #ff2d55 0%, {bar_color} 100%);
                            box-shadow: 0 0 15px {glow_color}; border-radius:2px;">
                </div>
                <div style="position:absolute; left:33%; top:0; height:100%;
                            width:1px; background:rgba(255,255,255,0.08);"></div>
                <div style="position:absolute; left:66%; top:0; height:100%;
                            width:1px; background:rgba(255,255,255,0.08);"></div>
            </div>
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem;
                        color:#2a3a4a; text-align:center; margin-top:0.3rem;">
                EXECUTIVE HEALTH INDEX
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Speedometer ──
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=efv_score,
            number={"font": {"family": "Orbitron", "size": 32, "color": "#00ffe1"}},
            title={"text": "EXECUTIVE FUNCTION VELOCITY",
                   "font": {"family": "Orbitron", "size": 11, "color": "#4a6278"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#1a2535",
                         "tickfont": {"family": "Share Tech Mono", "size": 9, "color": "#2a3a4a"}},
                "bar": {"color": "#00ffe1", "thickness": 0.2},
                "bgcolor": "#080c10",
                "borderwidth": 1, "bordercolor": "#1a2535",
                "steps": [
                    {"range": [0,  33], "color": "rgba(255,45,85,0.2)"},
                    {"range": [33, 66], "color": "rgba(255,215,0,0.15)"},
                    {"range": [66,100], "color": "rgba(57,255,20,0.15)"},
                ],
            },
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=250, margin=dict(t=50, b=10, l=30, r=30),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # ── Dominant + Emotion bars ──
        st.markdown(f"""
        <div style="font-family:'Share Tech Mono',monospace; font-size:0.7rem;
                    color:#4a6278; letter-spacing:0.2em; margin-bottom:0.8rem;">
            DOMINANT SIGNAL:
            <span style="color:#00ffe1; font-size:0.9rem;"> {dominant.upper()}</span>
        </div>
        """, unsafe_allow_html=True)

        emotion_colors = {
            "joy": "#39ff14", "sadness": "#4488ff", "anger": "#ff2d55",
            "fear": "#ff8c00", "surprise": "#ffd700", "disgust": "#bf5af2",
        }
        for emotion, score in sorted(emotions.items(), key=lambda x: -x[1]):
            pct   = score * 100
            color = emotion_colors.get(emotion, "#00ffe1")
            st.markdown(f"""
            <div style="margin-bottom:0.6rem;">
                <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
                    <span style="font-family:'Share Tech Mono',monospace; font-size:0.65rem;
                                 color:#4a6278;">{emotion.upper()}</span>
                    <span style="font-family:'Share Tech Mono',monospace; font-size:0.65rem;
                                 color:{color};">{pct:.1f}%</span>
                </div>
                <div style="height:6px; background:#0a0f14; border-radius:2px; overflow:hidden;">
                    <div style="height:100%; width:{pct}%; background:{color}; border-radius:2px;">
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Somatic Protocol ──
        st.markdown(f"""
        <div style="margin-top:1.5rem; background:#080c10;
                    border:1px solid {bio['color']}55; border-radius:4px;
                    padding:1.3rem 1.4rem;">
            <div style="font-family:'Orbitron',monospace; font-size:0.6rem;
                        color:{bio['color']}; letter-spacing:0.3em; margin-bottom:0.6rem;">
                ⚑ NEUROCHEMICAL DIAGNOSIS
            </div>
            <div style="font-family:'Orbitron',monospace; font-size:0.9rem; font-weight:700;
                        color:{bio['color']}; margin-bottom:0.6rem;">
                {bio['label']}
            </div>
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.78rem;
                        color:#7ecfca; line-height:1.7; margin-bottom:1.2rem;">
                {bio['detail']}
            </div>
            <div style="font-family:'Orbitron',monospace; font-size:0.6rem;
                        color:{bio['color']}; letter-spacing:0.25em; margin-bottom:0.6rem;">
                ⬡ SOMATIC PROTOCOL
            </div>
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.78rem;
                        color:#e8f4f8; line-height:2; white-space:pre-line;">
                {bio['protocol']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("✅ VERIFY RESET"):
            st.markdown("""
            <div style="margin-top:1rem; background:#001a0a; border:1px solid #39ff14;
                        border-radius:4px; padding:0.8rem 1.2rem; text-align:center;
                        font-family:'Orbitron',monospace; font-size:0.75rem;
                        color:#39ff14; letter-spacing:0.2em;">
                ✓ SOMATIC RESET VERIFIED — SYSTEM RECALIBRATING
            </div>
            """, unsafe_allow_html=True)
            # ── Audio Summary ──
        st.markdown("""
        <div style="font-family:'Orbitron',monospace; font-size:0.6rem;
                    color:#2a3a4a; letter-spacing:0.25em; margin: 1rem 0 0.5rem;">
            ▸ AUDIO SUMMARY
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔊 SYNTHESIZE AUDIO"):
            with st.spinner("SYNTHESIZING VOICEOVER..."):
                audio_bytes = synthesize(bio, dominant)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.caption("TTS unavailable — install pyttsx3")

# ════════════════════════════════════════
# RIGHT COLUMN
# ════════════════════════════════════════
with right:

    st.markdown("""
    <div style="font-family:'Orbitron',monospace; font-size:0.65rem; color:#4a6278;
                letter-spacing:0.3em; margin-bottom:1rem;">
        ▸ LIVE PSYCHE FEED
    </div>
    """, unsafe_allow_html=True)

    # Get feed — use result if available, else show defaults
    if st.session_state.result:
        feed_items = st.session_state.result["feed"]
    else:
        from engine.scraper import get_feed
        feed_items = get_feed("sadness")  # default state

    type_colors = {"jung": "#bf5af2", "neuro": "#00ffe1"}
    type_labels = {"jung": "JUNG",    "neuro": "NEURO"}

    for item in feed_items:
        color = type_colors.get(item["type"], "#00ffe1")
        label = type_labels.get(item["type"], "FEED")

        st.markdown(f"""
        <div style="background:#080c10; border:1px solid #1a2535;
                    border-left:2px solid {color}; border-radius:0 4px 4px 0;
                    padding:0.9rem 1rem; margin-bottom:0.8rem;">
            <div style="font-family:'Orbitron',monospace; font-size:0.5rem;
                        color:{color}; letter-spacing:0.25em; margin-bottom:0.4rem;">
                ▸ {label}
            </div>
            <div style="font-family:'Share Tech Mono',monospace; font-size:0.8rem;
                        color:#7ecfca; line-height:1.6;
                        font-style:{'italic' if item['type'] == 'jung' else 'normal'};">
                {item['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)