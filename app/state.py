from typing import TypedDict, Optional

class AgentState(TypedDict):
    """Defines the internal state passed dynamically across LangGraph nodes."""
    input_text: str
    normalized_text: Optional[str]
    predicted_emotion: Optional[str]
    confidence_score: Optional[float]
    retry_count: int
    is_valid: bool
    error_log: Optional[str]