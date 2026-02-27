from typing import TypedDict

class InvestigationState(TypedDict):

    # Input
    input_type: str
    content: str

    # Detective 1 Output
    extracted_claims: list

    # Detective 2 Output
    claim_results: list
    fact_check_score: int

    # Detective 3 Output
    image_url: str
    exif_data: dict
    image_flags: list
    image_score: int

    # Detective 4 Output
    emotional_triggers: list
    author_found: bool
    source_credibility: str
    manipulation_score: int
    language_score: int

    # Detective 5 Output
    total_score: int
    verdict: str
    verdict_type: str
    confidence: int
    explanation: str
    flags: list