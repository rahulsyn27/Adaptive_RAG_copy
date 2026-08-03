"""
Route identifier model for query classification.
"""

from pydantic import BaseModel, Field


class RouteIdentifier(BaseModel):
    """Query classification result."""

    classification: str = Field(
        description="Route classification: 'index', 'general', or 'search'"
    )