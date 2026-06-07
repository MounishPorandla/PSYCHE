def compute_bio_state(emotions):
    """
    Reads emotion scores, returns a diagnosis + what to DO about it.
    """
    fear    = emotions.get("fear", 0)
    sadness = emotions.get("sadness", 0)
    anger   = emotions.get("anger", 0)
    joy     = emotions.get("joy", 0)
    surprise = emotions.get("surprise", 0)

    # ── Decide which state the nervous system is in ──

    # State 1: Freeze/Paralysis
    if fear > 0.3 or sadness > 0.4:
        return {
            "label":    "HIGH CORTISOL / LOW DOPAMINE PARALYSIS",
            "color":    "#ff2d55",
            "detail":   "Your amygdala has partially hijacked prefrontal access. "
                        "Cortisol is elevated. You cannot think your way out of this — "
                        "the body has to move first.",
            "protocol": (
                "1. Stand up right now.\n"
                "2. Do 10 explosive jumping jacks — arms fully extended.\n"
                "3. Then take 5 slow exhales through your mouth.\n"
                "4. Drink cold water if you have it.\n"
                "5. Click VERIFY RESET below."
            ),
            "short": "Do 10 jumping jacks, then 5 slow exhales.",
        }

    # State 2: Scattered/Overdrive
    if anger > 0.3 or surprise > 0.4:
        return {
            "label":    "NOREPINEPHRINE OVERDRIVE / ATTENTION SCATTER",
            "color":    "#ffd700",
            "detail":   "Your brain is firing in too many directions. "
                        "High arousal without a channel. "
                        "Forcing output right now produces noise, not work.",
            "protocol": (
                "1. Write down the ONE task that matters today.\n"
                "2. Set a 25 minute timer. Phone face down.\n"
                "3. Close every tab except the one you need.\n"
                "4. Do 4-7-8 breathing: inhale 4s, hold 7s, exhale 8s. Three times.\n"
                "5. Click VERIFY RESET below."
            ),
            "short": "Write your one task, then do 4-7-8 breathing three times.",
        }

    # State 3: Flow
    if joy > 0.4:
        return {
            "label":    "DOPAMINE FLOW / HYPERFOCUS WINDOW",
            "color":    "#39ff14",
            "detail":   "Reward circuits are online. Prefrontal cortex accessible. "
                        "This is the rare window. It is finite. Protect it.",
            "protocol": (
                "1. Block all notifications right now.\n"
                "2. Water and snack within reach.\n"
                "3. Set a 90 minute timer.\n"
                "4. Do not open social media — it will end this state instantly.\n"
                "5. Click VERIFY RESET to confirm environment is locked."
            ),
            "short": "Block notifications and protect the next 90 minutes.",
        }

    # State 4: Default / Processing
    return {
        "label":    "INTEGRATION STATE / PROCESSING MODE",
        "color":    "#00ffe1",
        "detail":   "System is neither frozen nor fully online. "
                    "Prefrontal cortex is partially available. "
                    "Don't force big output. Warm the engine.",
        "protocol": (
            "1. Do 5 minutes of any movement — walk, stretch, pace.\n"
            "2. Write two sentences: what you need and what's blocking it.\n"
            "3. Pick your smallest possible first action.\n"
            "4. Do only that. Nothing else.\n"
            "5. Click VERIFY RESET below."
        ),
        "short": "Move for 5 minutes, then find your smallest possible next action.",
    }