from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from src.schemas.state import State
from src.config.prompts import SystemPrompts
from src.schemas.models import UserProfile
from src.llm.azure_openai import AzureOpenAI


class CreateMemoryNode:
    """
    Node class for analyzing conversations and managing user memory profiles.

    This node is responsible for extracting and updating user music preferences
    from conversation history and storing them in long-term memory.
    """

    def __init__(self):
        """Initialize the CreateMemoryNode."""
        pass

    def _initialize_llm(self, config: RunnableConfig):
        """Initialize the Azure OpenAI instance."""

        self.llm = AzureOpenAI.get_instance(config["settings"])
        self.structured_llm = self.llm.get_structured_llm(UserProfile)

    def _get_existing_memory(self, store: BaseStore, customer_id: str) -> str:
        """
        Retrieve existing memory profile for the user.

        Args:
            store: The store for conversation data
            customer_id: The customer ID

        Returns:
            str: Formatted memory string for prompt injection
        """
        namespace = ("memory_profile", customer_id)
        existing_memory = store.get(namespace, "user_memory")

        if existing_memory and existing_memory.value:
            existing_memory_dict = existing_memory.value
            music_preferences = (
                existing_memory_dict.get("memory").music_preferences or []
            )
            return f"Music Preferences: {', '.join(music_preferences)}"

        return ""

    def _analyze_conversation(self, state: State, formatted_memory: str) -> UserProfile:
        """
        Analyze conversation using structured LLM to extract memory updates.

        Args:
            state: Current conversation state
            formatted_memory: Existing memory profile as formatted string

        Returns:
            UserProfile: Updated memory profile
        """
        formatted_system_message = SystemMessage(
            content=SystemPrompts.memory_creation_prompt().format(
                conversation=state["messages"], memory_profile=formatted_memory
            )
        )

        return self.structured_llm.invoke([formatted_system_message])

    def _store_memory(
        self, store: BaseStore, customer_id: str, updated_memory: UserProfile
    ):
        """
        Store the updated memory profile in long-term storage.

        Args:
            store: The store for conversation data
            customer_id: The customer ID
            updated_memory: Updated UserProfile to store
        """
        namespace = ("memory_profile", customer_id)
        key = "user_memory"
        store.put(namespace, key, {"memory": updated_memory})

    def execute(self, state: State, config: RunnableConfig, store: BaseStore) -> dict:
        """
        Analyze the conversation and save/update user music preferences.

        Args:
            state: The current state of the conversation
            config: The configuration for the conversation
            store: The store for the conversation

        Returns:
            dict: The updated memory profile
        """
        # Initialize LLM components
        self._initialize_llm(config)

        # Get the customer ID from the current state
        customer_id = str(state["customer_id"])

        # Get existing memory profile for this user
        formatted_memory = self._get_existing_memory(store, customer_id)

        # Analyze conversation and extract updated memory
        updated_memory = self._analyze_conversation(state, formatted_memory)

        # Store the updated memory profile
        self._store_memory(store, customer_id, updated_memory)

        # Return the updated memory profile
        return {"loaded_memory": updated_memory}
