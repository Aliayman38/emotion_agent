from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.tools import normalize_arabic_text, call_emotion_classifier_llm
from app.logger import logger

def normalize_text_node(state: AgentState) -> AgentState:
    """Node that targets processing, clean up, and standardization of raw input strings."""
    logger.info("Entering Node: [Normalize Text Node]")
    raw_input = state["input_text"]
    normalized = normalize_arabic_text(raw_input)
    
    state["normalized_text"] = normalized
    return state

def classify_emotion_node(state: AgentState) -> AgentState:
    """Node responsible for communicating with the underlying LLM layer."""
    logger.info("Entering Node: [Classify Emotion Node]")
    target_text = state["normalized_text"] or state["input_text"]
    
    result = call_emotion_classifier_llm(target_text)
    
    state["predicted_emotion"] = result["emotion"]
    state["confidence_score"] = result["confidence"]
    state["error_log"] = result["error"]
    
    return state

def validate_output_node(state: AgentState) -> AgentState:
    """Node that runs algorithmic assertion checks against validation boundaries."""
    logger.info("Entering Node: [Validate Output Node]")
    
    allowed_classes = {"happy", "sad", "angry", "neutral"}
    emotion = state.get("predicted_emotion")
    confidence = state.get("confidence_score", 0.0)
    has_error = state.get("error_log") is not None
    
    # Run absolute data matrix validation
    if not has_error and emotion in allowed_classes and (0.0 <= confidence <= 1.0):
        state["is_valid"] = True
        logger.info("Validation Succeeded: Parameters fit operational range bounds.")
    else:
        state["is_valid"] = False
        state["retry_count"] += 1
        logger.warning(
            f"Validation Failed: (Emotion: {emotion}, Confidence: {confidence}, Error: {state.get('error_log')}). "
            f"Retry sequence adjusted to: {state['retry_count']}"
        )
        
    return state

def route_conditional_edge(state: AgentState) -> str:
    """Determines programmatic routing depending on validation state parameters."""
    if state["is_valid"]:
        return "end"
    elif state["retry_count"] <= 1:
        logger.info("Routing logic triggering system structural retry cycle.")
        return "retry"
    else:
        logger.error("Max retries exceeded or catastrophic validation failure. Terminating pipeline.")
        return "end"

# Build StateGraph Layout Configuration
workflow = StateGraph(AgentState)

# Append Functional Processing Nodes
workflow.add_node("normalize_text", normalize_text_node)
workflow.add_node("classify_emotion", classify_emotion_node)
workflow.add_node("validate_output", validate_output_node)

# Set Pipeline Trajectory Structure
workflow.set_entry_point("normalize_text")
workflow.add_edge("normalize_text", "classify_emotion")
workflow.add_edge("classify_emotion", "validate_output")

# Build Conditional Verification Loop
workflow.add_conditional_edges(
    "validate_output",
    route_conditional_edge,
    {
        "retry": "classify_emotion",
        "end": END
    }
)

# Compile Executable Application Graph
agent_graph = workflow.compile()