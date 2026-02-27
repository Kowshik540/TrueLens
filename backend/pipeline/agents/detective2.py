import os
import json
from dotenv import load_dotenv
from groq import Groq
from pipeline.state import InvestigationState
from tools.serper_search import search_claim

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def detective2(state: InvestigationState) -> InvestigationState:
    """
    Detective 2 — Fact Verifier (Improved)
    Verifies claims using search + LLM with partial scoring.
    """
    print("\nDetective 2 — Verifying claims...")

    claims = state.get("extracted_claims", [])

    if not claims:
        print("Detective 2 — No claims to verify")
        return {**state, "claim_results": [], "fact_check_score": 5}  # baseline

    claim_results = []
    verified_count = 0
    partial_count = 0

    for i, claim in enumerate(claims):
        print(f"  Checking claim {i+1}: {claim[:60]}...")

        search_results = search_claim(claim)

        if not search_results:
            claim_results.append({
                "claim": claim,
                "verdict": "NOT FOUND",
                "evidence": "No search results returned",
                "score": 0
            })
            continue

        results_text = ""
        for r in search_results[:3]:
            results_text += f"- {r.get('title','')}: {r.get('snippet','')}\n"

        prompt = f"""
You are a professional fact-checker.
Classify the claim based on the evidence.

Claim: {claim}

Search Results:
{results_text}

Return ONLY valid JSON:
{{
  "verdict": "VERIFIED" or "CONTRADICTED" or "PARTIALLY VERIFIED" or "NOT FOUND",
  "evidence": "one short sentence"
}}
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )

            raw = response.choices[0].message.content.strip()

            # Clean markdown
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]

            result = json.loads(raw)
            verdict = result.get("verdict", "NOT FOUND").upper()
            evidence = result.get("evidence", "")

            score = 0
            if verdict == "VERIFIED":
                score = 1
                verified_count += 1
            elif verdict == "PARTIALLY VERIFIED":
                score = 0.5
                partial_count += 1

            claim_results.append({
                "claim": claim,
                "verdict": verdict,
                "evidence": evidence,
                "score": score
            })

            print(f"    → {verdict}: {evidence}")

        except Exception as e:
            print(f"    → Error checking claim: {e}")
            claim_results.append({
                "claim": claim,
                "verdict": "NOT FOUND",
                "evidence": "Verification failed",
                "score": 0
            })

    # --- Smarter scoring ---
    total_points = verified_count + (partial_count * 0.5)
    fact_check_score = int((total_points / len(claims)) * 40)

    # baseline so it never collapses to 0 for real articles
    if fact_check_score == 0 and len(claims) > 0:
        fact_check_score = 8

    print(f"\nDetective 2 — Verified: {verified_count}, Partial: {partial_count}")
    print(f"Detective 2 — Fact check score: {fact_check_score}/40")

    return {**state, "claim_results": claim_results, "fact_check_score": fact_check_score}
