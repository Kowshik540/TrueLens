import os
import json
from dotenv import load_dotenv
from groq import Groq
from pipeline.state import InvestigationState

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def detective4(state: InvestigationState) -> InvestigationState:
    print("\nDetective 4 — Analyzing language...")

    content = state["content"]
    text = content.lower()

    # Rule-based signals
    sensational_words = ["shocking", "breaking", "you won't believe", "must read", "share before deleted"]
    found_triggers = [w for w in sensational_words if w in text]

    flags = []
    score = 30

    if found_triggers:
        score -= 10
        flags.append("Sensational language detected")

    if text.count("!") > 5:
        score -= 5
        flags.append("Excessive exclamation marks")

    if "according to sources" in text or "insiders say" in text:
        score -= 5
        flags.append("Vague sources used")

    # LLM for deeper nuance
    prompt = f"""
Analyze writing credibility and return JSON:
{{
  "author_found": true or false,
  "source_credibility": "STRONG" or "WEAK" or "VAGUE",
  "manipulation_score": 0-100,
  "extra_flags": ["flag one", "flag two"]
}}

Article:
{content}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        raw = response.choices[0].message.content.strip()
        if "```" in raw:
            raw = raw.split("```")[1].replace("json", "").strip()

        result = json.loads(raw)

        author_found       = result.get("author_found", False)
        source_credibility = result.get("source_credibility", "VAGUE")
        manipulation_score = int(result.get("manipulation_score", 50))
        flags.extend(result.get("extra_flags", []))

        if not author_found:
            score -= 5
            flags.append("No author info")

        if source_credibility == "WEAK":
            score -= 5
        elif source_credibility == "VAGUE":
            score -= 3

    except:
        author_found = False
        source_credibility = "VAGUE"
        manipulation_score = 50

    score = max(0, min(score, 30))

    return {
        **state,
        "emotional_triggers": found_triggers,
        "author_found": author_found,
        "source_credibility": source_credibility,
        "manipulation_score": manipulation_score,
        "language_score": score,
        "flags": list(set(flags))
    }
