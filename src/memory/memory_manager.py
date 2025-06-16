"""Memory manager for coordinating short-term and long-term memory."""

from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore
from .short_term import ShortTermMemory
from .long_term import LongTermMemory


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

    def save_user_memory(self, user_id: str, memory_data: dict):
        """Save user memory to long-term storage."""
        return self.long_term.save_memory(user_id, memory_data)

    def load_user_memory(self, user_id: str) -> dict:
        """Load user memory from long-term storage."""
        return self.long_term.load_memory(user_id)

    def clear_conversation(self, thread_id: str):
        """Clear short-term conversation memory."""
        return self.short_term.clear_conversation(thread_id)

    def clear_user_memory(self, user_id: str):
        """Clear long-term user memory."""
        return self.long_term.clear_memory(user_id)
