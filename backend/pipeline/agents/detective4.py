import os
import json
from dotenv import load_dotenv
from groq import Groq
from pipeline.state import InvestigationState

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def detective4(state: InvestigationState) -> InvestigationState:
    """
    Detective 4 — Language Analyst
    Analyzes the writing style of the article to detect
    emotional manipulation, missing author info, vague sources,
    and logical contradictions.
    """
    print("\nDetective 4 — Analyzing language...")

    content = state["content"]

    prompt = f"""
You are a language manipulation expert analyzing a news article.

Analyze the following article for these 5 things:
1. Emotional trigger words (SHOCKING, BREAKING, Share before deleted, etc.)
2. Author information (is there a named author with credentials?)
3. Source credibility (are sources named specifically or vague like "insiders say")
4. Logical consistency (does the article contradict itself?)
5. Overall writing pattern (does it match known fake news style?)

Article:
{content}

Reply with ONLY a valid JSON object in this exact format:
{{
  "emotional_triggers": ["word1", "word2"],
  "author_found": true or false,
  "source_credibility": "STRONG" or "WEAK" or "VAGUE",
  "manipulation_score": 0,
  "language_score": 0,
  "flags": ["flag one", "flag two"]
}}

For manipulation_score (0-100):
- 0-20: very professional, no manipulation detected
- 21-40: minor concerns
- 41-60: moderate manipulation
- 61-80: strong manipulation signs
- 81-100: clear fake news writing patterns

For language_score out of 30:
- 25-30: clean professional writing
- 15-24: some concerns
- 5-14: strong manipulation detected
- 0-4: matches fake news patterns very closely
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        raw = response.choices[0].message.content.strip()

        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        result = json.loads(raw)

        emotional_triggers = result.get("emotional_triggers", [])
        author_found       = result.get("author_found", False)
        source_credibility = result.get("source_credibility", "VAGUE")
        manipulation_score = int(result.get("manipulation_score", 50))
        language_score     = int(result.get("language_score", 15))
        flags              = result.get("flags", [])

        print(f"Detective 4 — Emotional triggers: {emotional_triggers}")
        print(f"Detective 4 — Author found: {author_found}")
        print(f"Detective 4 — Source credibility: {source_credibility}")
        print(f"Detective 4 — Manipulation score: {manipulation_score}/100")
        print(f"Detective 4 — Language score: {language_score}/30")

        return {
            **state,
            "emotional_triggers": emotional_triggers,
            "author_found":       author_found,
            "source_credibility": source_credibility,
            "manipulation_score": manipulation_score,
            "language_score":     language_score,
            "flags":              flags
        }

    except Exception as e:
        print(f"Detective 4 error: {e}")
        return {
            **state,
            "emotional_triggers": [],
            "author_found":       False,
            "source_credibility": "VAGUE",
            "manipulation_score": 50,
            "language_score":     15,
            "flags":              []
        }