"""
Query request model for API endpoints.
"""

from pydantic import BaseModel


class QueryRequest(BaseModel):
    """Request model for RAG queries."""

    query: str