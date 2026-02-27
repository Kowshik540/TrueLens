from typing import TypedDict, Optional

class InvestigationState(TypedDict):

    # ── Input ──────────────────────────────────────────
    input_type: str          # "text" or "url"
    content: str             # the raw article text or URL

    # ── Detective 1 Output ─────────────────────────────
    extracted_claims: list   # list of strings

    # ── Detective 2 Output ─────────────────────────────
    claim_results: list      # list of dicts
    fact_check_score: int    # out of 40

    # ── Detective 3 Output ─────────────────────────────
    image_url: str           # first image found
    exif_data: dict          # raw metadata
    image_flags: list        # list of strings
    image_score: int         # out of 30

    # ── Detective 4 Output ─────────────────────────────
    emotional_triggers: list # list of strings
    author_found: bool
    source_credibility: str
    manipulation_score: int  # 0-100
    language_score: int      # out of 30

    # ── Detective 5 Output ─────────────────────────────
    total_score: int         # out of 100
    verdict: str             # REAL NEWS / MISLEADING / FAKE NEWS
    verdict_type: str        # real / misleading / fake
    confidence: int          # percentage
    explanation: str         # written explanation
    flags: list              # final combined evidence flags
