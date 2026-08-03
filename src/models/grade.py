"""
Grade model for document relevance scoring.
"""

from pydantic import BaseModel, Field


class Grade(BaseModel):
    """Binary relevance grade for retrieved documents."""

    binary_score: str = Field(
        description="Relevance score: 'yes' if relevant, 'no' if not relevant"
    )