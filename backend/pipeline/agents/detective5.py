import os
import json
from dotenv import load_dotenv
from groq import Groq
from pipeline.state import InvestigationState

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def detective5(state: InvestigationState) -> InvestigationState:
    """
    Detective 5 — The Judge
    Reads all 4 agent reports, calculates final weighted score,
    determines verdict, and writes full explanation.
    """
    print("\nDetective 5 — Calculating final verdict...")

    fact_check_score = state["fact_check_score"]
    image_score      = state["image_score"]
    language_score   = state["language_score"]
    claim_results    = state["claim_results"]
    image_flags      = state["image_flags"]
    emotional_triggers = state["emotional_triggers"]
    author_found     = state["author_found"]
    source_credibility = state["source_credibility"]
    manipulation_score = state["manipulation_score"]

    # Calculate total score
    total_score = fact_check_score + image_score + language_score

    # Determine verdict
    if total_score >= 80:
        verdict      = "REAL NEWS"
        verdict_type = "real"
        confidence   = total_score
    elif total_score >= 50:
        verdict      = "MISLEADING"
        verdict_type = "misleading"
        confidence   = 100 - abs(total_score - 65)
    else:
        verdict      = "FAKE NEWS"
        verdict_type = "fake"
        confidence   = 100 - total_score

    print(f"Detective 5 — Total score: {total_score}/100")
    print(f"Detective 5 — Verdict: {verdict}")
    print(f"Detective 5 — Confidence: {confidence}%")

    # Build summary of all findings for explanation prompt
    claim_summary = ""
    for r in claim_results:
        claim_summary += f"- {r['claim']}: {r['verdict']}\n"

    prompt = f"""
You are a senior fact-checker writing a final investigation report.

Here are the findings from all detectives:

FACT CHECK RESULTS (score {fact_check_score}/40):
{claim_summary if claim_summary else "No claims were verified"}

IMAGE FORENSICS (score {image_score}/30):
{chr(10).join(image_flags) if image_flags else "No image issues found"}

LANGUAGE ANALYSIS (score {language_score}/30):
- Emotional triggers found: {emotional_triggers}
- Author found: {author_found}
- Source credibility: {source_credibility}
- Manipulation score: {manipulation_score}/100

FINAL SCORE: {total_score}/100
VERDICT: {verdict}

Write a clear 3-4 sentence explanation of why this article received this verdict.
Be specific about which evidence was strongest.
Do not use bullet points. Write in plain paragraph form.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        explanation = response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Detective 5 explanation error: {e}")
        explanation = f"This article scored {total_score}/100. Verdict: {verdict}."

    # Build final flags list combining all agent findings
    final_flags = []

    for r in claim_results:
        flag_type = "teal" if r["verdict"] == "VERIFIED" else "red"
        final_flags.append({
            "text": f"{r['verdict']}: {r['claim']}",
            "type": flag_type
        })

    for f in image_flags:
        final_flags.append({"text": f, "type": "red"})

    if emotional_triggers:
        final_flags.append({
            "text": f"Emotional triggers detected: {', '.join(emotional_triggers)}",
            "type": "red"
        })

    if not author_found:
        final_flags.append({
            "text": "No author name or credentials found",
            "type": "gold"
        })

    if source_credibility in ["WEAK", "VAGUE"]:
        final_flags.append({
            "text": f"Source credibility: {source_credibility}",
            "type": "gold"
        })

    print(f"Detective 5 — Generated {len(final_flags)} evidence flags")

    return {
        **state,
        "total_score": total_score,
        "verdict":     verdict,
        "verdict_type": verdict_type,
        "confidence":  confidence,
        "explanation": explanation,
        "flags":       final_flags
    }