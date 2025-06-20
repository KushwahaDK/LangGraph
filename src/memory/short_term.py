"""Short-term memory implementation for conversation context."""

from langgraph.checkpoint.memory import MemorySaver


class ShortTermMemory:
    """Manages short-term memory within a single conversation thread."""

    def __init__(self):
        """Initialize short-term memory with MemorySaver."""
        self._checkpointer = MemorySaver()

    def get_checkpointer(self):
        """Get the checkpointer for maintaining conversation state."""
        return self._checkpointer
