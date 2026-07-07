from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional

class PredictRequest(BaseModel):
    """Input validation schema for API requests."""
    text: str = Field(..., min_length=1, description="The Arabic text sentence to analyze.")

    @field_validator('text')
    def check_empty_or_whitespace(cls, v):
        if not v.strip():
            raise ValueError("Input text cannot be empty or purely whitespace.")
        return v

class PredictResponse(BaseModel):
    """Output structural validation schema for API responses."""
    emotion: Literal["happy", "sad", "angry", "neutral"]
    confidence: float = Field(..., ge=0.0, le=1.0)

class LLMEmotionOutput(BaseModel):
    """Schema enforced on the LLM structured output payload."""
    emotion: str = Field(..., description="Must be one of: happy, sad, angry, neutral")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0")