from langgraph.graph import StateGraph, END
from pipeline.state import InvestigationState
from pipeline.agents.detective1 import detective1
from pipeline.agents.detective2 import detective2
from pipeline.agents.detective3 import detective3
from pipeline.agents.detective4 import detective4
from pipeline.agents.detective5 import detective5

def build_graph():
    """
    Builds and compiles the LangGraph pipeline.
    All 5 detectives connected in sequence.
    Each agent reads and writes to the shared InvestigationState.
    """

    graph = StateGraph(InvestigationState)

    # Add all 5 detective nodes
    graph.add_node("detective1", detective1)
    graph.add_node("detective2", detective2)
    graph.add_node("detective3", detective3)
    graph.add_node("detective4", detective4)
    graph.add_node("detective5", detective5)

    # Connect them in order
    graph.set_entry_point("detective1")
    graph.add_edge("detective1", "detective2")
    graph.add_edge("detective2", "detective3")
    graph.add_edge("detective3", "detective4")
    graph.add_edge("detective4", "detective5")
    graph.add_edge("detective5", END)

    return graph.compile()


# Build once at import time
investigation_graph = build_graph()


def run_investigation(input_type: str, content: str) -> dict:
    """
    Takes input type and content.
    Runs the full 5-agent pipeline.
    Returns the final state as a dict.
    """

    # Initial state — all fields set to defaults
    initial_state = {
        "input_type":          input_type,
        "content":             content,
        "extracted_claims":    [],
        "claim_results":       [],
        "fact_check_score":    0,
        "image_url":           "",
        "exif_data":           {},
        "image_flags":         [],
        "image_score":         0,
        "emotional_triggers":  [],
        "author_found":        False,
        "source_credibility":  "",
        "manipulation_score":  0,
        "language_score":      0,
        "total_score":         0,
        "verdict":             "",
        "verdict_type":        "",
        "confidence":          0,
        "explanation":         "",
        "flags":               []
    }

    final_state = investigation_graph.invoke(initial_state)
    return final_state