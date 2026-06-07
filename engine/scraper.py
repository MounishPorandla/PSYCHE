import random

# Content library keyed by dominant emotion
FEED_CONTENT = {
    "fear": [
        {"type": "jung",  "text": "Until you make the unconscious conscious, it will direct your life and you will call it fate. — Carl Jung"},
        {"type": "neuro", "text": "CORTISOL ALERT: Chronic fear keeps the amygdala semi-activated, gradually eroding the hippocampus. The threat is the loop itself, not the original trigger."},
        {"type": "jung",  "text": "The most terrifying thing is to accept oneself completely. — Carl Jung"},
    ],
    "sadness": [
        {"type": "jung",  "text": "Even a happy life cannot be without a measure of darkness. The word happy would lose its meaning if it were not balanced by sadness. — Carl Jung"},
        {"type": "neuro", "text": "SEROTONIN NOTE: 90% of the body's serotonin is produced in the gut, not the brain. Your emotional baseline is partly a digestion problem."},
        {"type": "jung",  "text": "Knowing your own darkness is the best method for dealing with the darknesses of other people. — Carl Jung"},
    ],
    "anger": [
        {"type": "jung",  "text": "Everything that irritates us about others can lead us to an understanding of ourselves. — Carl Jung"},
        {"type": "neuro", "text": "NOREPINEPHRINE SPIKE: Anger activates the same dopaminergic reward pathways as achievement. The brain finds righteous anger neurochemically satisfying — which is why it becomes addictive."},
    ],
    "joy": [
        {"type": "jung",  "text": "The privilege of a lifetime is to become who you truly are. — Carl Jung"},
        {"type": "neuro", "text": "FLOW STATE: Hyperfocus correlates with increased theta-wave activity in the prefrontal cortex. Your brain in flow is running a fundamentally different program."},
    ],
    "surprise": [
        {"type": "neuro", "text": "NOVELTY SIGNAL: Surprise triggers a dopamine spike even before reward delivery. Your brain is literally wired to reward the unexpected."},
        {"type": "jung",  "text": "In all chaos there is a cosmos, in all disorder a secret order. — Carl Jung"},
    ],
    "disgust": [
        {"type": "neuro", "text": "DISGUST-SHAME PATHWAY: Disgust and moral shame activate overlapping brain regions. The body doesn't distinguish between rotting food and perceived moral failure."},
        {"type": "jung",  "text": "The most intense conflicts, if overcome, leave behind a sense of security and calm that is not easily disturbed. — Carl Jung"},
    ],
}

FALLBACK = [
    {"type": "neuro", "text": "DEFAULT MODE NETWORK: When unfocused, your brain consumes 60-80% of its total energy on mind-wandering. Doing nothing is metabolically expensive."},
    {"type": "jung",  "text": "Who looks outside, dreams. Who looks inside, awakes. — Carl Jung"},
    {"type": "neuro", "text": "ADHD RESEARCH: The ADHD brain's reward signal fires differently — not weaker overall, but with higher sensitivity to immediacy. Delayed rewards barely register neurochemically."},
    {"type": "jung",  "text": "We cannot change anything unless we accept it. — Carl Jung"},
]


def get_feed(dominant_emotion, n=4):
    """
    Returns n feed items matched to the dominant emotion.
    Always mixes emotion-specific + fallback content.
    """
    pool = FEED_CONTENT.get(dominant_emotion, []) + FALLBACK
    random.shuffle(pool)
    return pool[:n]