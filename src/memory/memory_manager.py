"""Memory manager for coordinating short-term and long-term memory."""

from .short_term import ShortTermMemory
from .long_term import LongTermMemory
from src.schemas.state import State


class MemoryManager:
    """Unified interface for managing both short-term and long-term memory."""

    def __init__(self, store_type: str = "memory"):
        """
        Initialize memory manager with specified storage backend.

        Args:
            store_type: Type of storage backend ("memory", "redis", "postgres")
        """
        self.store_type = store_type
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(store_type)

    def get_checkpointer(self):
        """Get the checkpointer for short-term memory."""
        return self.short_term.get_checkpointer()

    def get_store(self):
        """Get the store for long-term memory."""
        return self.long_term.get_store()

    def load_user_memory(self, state: State) -> dict:
        """Load user memory from long-term storage."""
        return self.long_term.load_memory(state)
