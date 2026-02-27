import os
import json
from dotenv import load_dotenv
from groq import Groq
from pipeline.state import InvestigationState

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def detective1(state: InvestigationState) -> InvestigationState:
    """
    Detective 1 — Claim Extractor
    Reads the article text and extracts every specific
    verifiable factual claim as a clean list.
    """
    print("Detective 1 — Extracting claims...")

    content = state["content"]

    prompt = f"""
You are a fact-checking assistant. Read the following article and extract every specific, verifiable factual claim.

Rules:
- Only extract claims that can be verified (facts, statistics, events, announcements, names, dates)
- Do NOT include opinions or vague statements
- Return ONLY a valid JSON array of strings, nothing else, no explanation
- Maximum 8 claims
- Each claim should be a short clear sentence

Article:
{content}

Return format example:
["claim one", "claim two", "claim three"]
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        raw = response.choices[0].message.content.strip()

        # Clean up in case model adds markdown code block
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        claims = json.loads(raw)

        if not isinstance(claims, list):
            claims = []

        print(f"Detective 1 — Found {len(claims)} claims")
        for i, c in enumerate(claims):
            print(f"  {i+1}. {c}")

        return {**state, "extracted_claims": claims}

    except Exception as e:
        print(f"Detective 1 error: {e}")
        return {**state, "extracted_claims": []}