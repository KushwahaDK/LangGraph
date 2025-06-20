"""Long-term memory implementation for user preferences and context."""

from src.schemas.state import State
from langgraph.store.memory import InMemoryStore
from typing import Dict, Any


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
        else:
            raise ValueError(f"Unsupported store type: {store_type}")

    def get_store(self):
        """Get the store instance."""
        return self._store

    def load_memory(self, state: State) -> dict:
        """
        Load user memory from long-term storage.

        Args:
            state: State containing customer_id

        Returns:
            User memory data or empty string if not found
        """
        customer_id = state["customer_id"]

        # Create a namespace for the user's memory
        namespace = ("memory_profile", customer_id)

        # Get the user memory from the store
        key = "user_memory"
        result = self._store.get(namespace, key)

        # If memory exists and has a value, format it using our helper function.
        if result and result.value:
            formatted_memory = self.format_user_memory(result.value)
        else:
            formatted_memory = ""

        # Update the `loaded_memory` field in the state with the retrieved and formatted memory.
        return {"loaded_memory": formatted_memory}

    def save_memory(self, state: State) -> dict:
        """
        Save user memory to long-term storage.

        Args:
            state: State containing customer_id

        Returns:
            User memory data or empty string if not found

        """
        # Get the customer_id from the state
        customer_id = state["customer_id"]
        namespace = ("memory_profile", customer_id)
        key = "user_memory"

        # Save the user memory to the store
        self._store.put(namespace, key, state["loaded_memory"])
        return {"loaded_memory": state["loaded_memory"]}

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
