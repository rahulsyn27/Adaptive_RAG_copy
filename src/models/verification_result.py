"""
Verification result model for answer faithfulness checking.
"""

from pydantic import BaseModel, Field


class VerificationResult(BaseModel):
    """Verification result for answer faithfulness."""

    faithful: bool = Field(description="Whether the answer is faithful to the context")
    explanation: str = Field(description="Explanation of the verification result")