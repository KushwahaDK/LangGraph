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

    def clear_conversation(self, thread_id: str):
        """
        Clear conversation memory for a specific thread.

        Args:
            thread_id: Thread identifier for the conversation
        """
        # MemorySaver doesn't have a direct clear method,
        # but this can be extended for other backends
        pass
