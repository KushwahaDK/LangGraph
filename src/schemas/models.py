"""Pydantic models for data validation and serialization."""

from pydantic import BaseModel, Field
from typing import List


class UserInput(BaseModel):
    """Schema for parsing user-provided account information."""

    identifier: str = Field(
        description="Identifier, which can be a customer ID, email, or phone number."
    )


class UserProfile(BaseModel):
    """User profile structure for long-term memory storage."""

    customer_id: str = Field(description="The customer ID of the customer")
    music_preferences: List[str] = Field(
        description="The music preferences of the customer", default_factory=list
    )
