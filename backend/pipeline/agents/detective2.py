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
    Detective 2 — Fact Verifier
    Takes each extracted claim and searches the internet
    to verify if it is true, false, or unverifiable.
    """
    print("\nDetective 2 — Verifying claims...")

    claims = state["extracted_claims"]

    if not claims:
        print("Detective 2 — No claims to verify")
        return {**state, "claim_results": [], "fact_check_score": 0}

    claim_results = []
    verified_count = 0

    for i, claim in enumerate(claims):
        print(f"  Checking claim {i+1}: {claim[:60]}...")

        # Search the internet for this claim
        search_results = search_claim(claim)

        if not search_results:
            claim_results.append({
                "claim": claim,
                "verdict": "NOT FOUND",
                "evidence": "No search results returned",
                "score": 0
            })
            continue

        # Format search results for Groq
        results_text = ""
        for r in search_results[:3]:
            results_text += f"- {r['title']}: {r['snippet']}\n"

        prompt = f"""
You are a fact-checker. Based on the search results below, determine if the claim is verified.

Claim: {claim}

Search Results:
{results_text}

Reply with ONLY a valid JSON object in this exact format:
{{
  "verdict": "VERIFIED" or "CONTRADICTED" or "NOT FOUND",
  "evidence": "one sentence explaining what you found"
}}
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
            verdict = result.get("verdict", "NOT FOUND")
            evidence = result.get("evidence", "")

            score = 0
            if verdict == "VERIFIED":
                score = 1
                verified_count += 1

            claim_results.append({
                "claim":    claim,
                "verdict":  verdict,
                "evidence": evidence,
                "score":    score
            })

            print(f"    → {verdict}: {evidence[:60]}")

        except Exception as e:
            print(f"    → Error checking claim: {e}")
            claim_results.append({
                "claim":    claim,
                "verdict":  "NOT FOUND",
                "evidence": "Could not verify",
                "score":    0
            })

    # Calculate fact check score out of 40
    if len(claims) > 0:
        fact_check_score = int((verified_count / len(claims)) * 40)
    else:
        fact_check_score = 0

    print(f"\nDetective 2 — {verified_count}/{len(claims)} claims verified")
    print(f"Detective 2 — Fact check score: {fact_check_score}/40")

    return {**state, "claim_results": claim_results, "fact_check_score": fact_check_score}