"""Input validation utilities."""

import re
from langchain_core.runnables import RunnableConfig
from src.schemas.state import State


def validate_customer_identifier(identifier: str) -> bool:
    """
    Validate customer identifier format.

    Args:
        identifier (str): Customer identifier to validate

    Returns:
        bool: True if identifier format is valid
    """
    if not identifier or not isinstance(identifier, str):
        return False

    # Check if it's a numeric customer ID
    if identifier.isdigit():
        return True

    # Check if it's a valid email format
    if "@" in identifier:
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(email_pattern, identifier))

    # Check if it's a phone number (starts with +)
    if identifier.startswith("+"):
        # Basic phone number validation
        phone_pattern = r"^\+\d[\d\s\(\)\-]{7,15}$"
        return bool(re.match(phone_pattern, identifier))

    return False


def sanitize_sql_input(value: str) -> str:
    """
    Basic SQL input sanitization.

    Args:
        value (str): Input value to sanitize

    Returns:
        str: Sanitized value
    """
    if not isinstance(value, str):
        return str(value)

    # Remove potentially dangerous characters
    dangerous_chars = ["'", '"', ";", "--", "/*", "*/", "xp_", "sp_"]
    sanitized = value

    for char in dangerous_chars:
        sanitized = sanitized.replace(char, "")

    return sanitized.strip()


def validate_query_parameters(params: dict) -> dict:
    """
    Validate and sanitize query parameters.

    Args:
        params (dict): Parameters to validate

    Returns:
        dict: Validated and sanitized parameters
    """
    validated = {}

    for key, value in params.items():
        if isinstance(value, str):
            validated[key] = sanitize_sql_input(value)
        else:
            validated[key] = value

    return validated


# Conditional edge: should_interrupt
def should_interrupt(state: State, config: RunnableConfig):
    """
    Determines whether the workflow should interrupt and ask for human input.

    If the customer_id is present in the state (meaning verification is complete),
    the workflow continues. Otherwise, it interrupts to get human input for verification.
    """
    if state.get("customer_id") is not None:
        return "continue"  # Customer ID is verified, continue to the next step (supervisor)
    else:
        return "interrupt"  # Customer ID is not verified, interrupt for human input
