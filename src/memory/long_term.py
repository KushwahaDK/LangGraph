"""Long-term memory implementation for user preferences and context."""

from langgraph.store.memory import InMemoryStore
from typing import Dict, Any, Optional


class LongTermMemory:
    """Manages long-term memory for user preferences and context."""

    def __init__(self, store_type: str = "memory"):
        """
        Initialize long-term memory with specified backend.

        Args:
            store_type: Type of storage backend ("memory", "redis", "postgres")
        """
        self.store_type = store_type
        self._store = self._create_store(store_type)

    def _create_store(self, store_type: str):
        """Create appropriate store based on type."""
        if store_type == "memory":
            return InMemoryStore()
        elif store_type == "redis":
            # TODO: Implement Redis store
            raise NotImplementedError("Redis store not yet implemented")
        elif store_type == "postgres":
            # TODO: Implement PostgreSQL store
            raise NotImplementedError("PostgreSQL store not yet implemented")
        else:
            raise ValueError(f"Unsupported store type: {store_type}")

    def get_store(self):
        """Get the store instance."""
        return self._store

    def save_memory(self, user_id: str, memory_data: Dict[str, Any]):
        """
        Save user memory to long-term storage.

        Args:
            user_id: User identifier
            memory_data: Memory data to save
        """
        namespace = ("memory_profile", user_id)
        key = "user_memory"
        self._store.put(namespace, key, memory_data)

    def load_memory(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Load user memory from long-term storage.

        Args:
            user_id: User identifier

        Returns:
            User memory data or None if not found
        """
        namespace = ("memory_profile", user_id)
        key = "user_memory"
        result = self._store.get(namespace, key)
        return result.value if result else None

    def clear_memory(self, user_id: str):
        """
        Clear user memory from long-term storage.

        Args:
            user_id: User identifier
        """
        namespace = ("memory_profile", user_id)
        key = "user_memory"
        # InMemoryStore doesn't have delete method, but this can be extended
        # for other backends that support deletion
        pass

    def format_user_memory(self, user_data: Dict[str, Any]) -> str:
        """
        Format user memory data for use in prompts.

        Args:
            user_data: Raw user memory data

        Returns:
            Formatted memory string
        """
        if not user_data or "memory" not in user_data:
            return ""

        profile = user_data["memory"]
        result = ""

        # Check if music_preferences attribute exists and is not empty
        if hasattr(profile, "music_preferences") and profile.music_preferences:
            result += f"Music Preferences: {', '.join(profile.music_preferences)}"

        return result.strip()
