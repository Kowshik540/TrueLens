from pipeline.state import InvestigationState

def detective5(state: InvestigationState) -> InvestigationState:
    """
    Detective 5 — Judge
    Combines all evidence into a final verdict.
    """

    fact  = state.get("fact_check_score", 0)    # /40
    image = state.get("image_score", 0)         # /30
    lang  = state.get("language_score", 0)      # /30

    total_score = fact + image + lang

    flags = []

    # Hard penalties
    if fact == 0:
        flags.append("No claims could be verified from trusted sources")

    if image < 10:
        flags.append("Image evidence is highly suspicious")

    if lang < 10:
        flags.append("Writing style strongly matches fake news patterns")

    # Verdict logic
    if fact >= 28 and total_score >= 75:
        verdict_type = "real"
        verdict = "REAL NEWS"
        confidence = min(95, total_score + 10)

    elif fact >= 15 and total_score >= 50:
        verdict_type = "misleading"
        verdict = "MISLEADING"
        confidence = min(85, total_score + 5)

    else:
        verdict_type = "fake"
        verdict = "FAKE NEWS"
        confidence = min(90, max(40, total_score + 20))

    explanation = (
        f"The article was evaluated across fact verification, image forensics, and language analysis. "
        f"It received a fact check score of {fact}/40, image score of {image}/30, and language score of {lang}/30. "
        f"These combined signals resulted in a total score of {total_score}/100 and a verdict of {verdict.lower()}."
    )

    return {
        **state,
        "total_score": total_score,
        "verdict": verdict,
        "verdict_type": verdict_type,
        "confidence": confidence,
        "flags": list(set(state.get("flags", []) + flags)),
        "explanation": explanation
    }
