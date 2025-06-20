from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from src.schemas.state import State
from src.config.prompts import SystemPrompts
from src.schemas.models import UserProfile
from src.llm.azure_openai import AzureOpenAI


# This node is responsible for analyzing the conversation and saving/updating user music preferences.
def create_memory(state: State, config: RunnableConfig, store: BaseStore) -> dict:
    """
    This node is responsible for analyzing the conversation and saving/updating user music preferences.

    Args:
        state: The current state of the conversation.
        config: The configuration for the conversation.
        store: The store for the conversation.
    Returns:
        The updated memory profile.
    """
    # Get the customer ID from the current state (convert to string).
    customer_id = str(state["customer_id"])

    # Define the namespace for this user's memory profile.
    namespace = (
        "memory_profile",
        customer_id,
    )  # Define the namespace for this user's memory profile.

    # Get the existing memory profile for this user from the long-term store.
    existing_memory = store.get(namespace, "user_memory")

    # Initialize formatted memory for the prompt.
    formatted_memory = ""  # Initialize formatted memory for the prompt.
    if existing_memory and existing_memory.value:
        # Get the dictionary containing the UserProfile instance.
        existing_memory_dict = (
            existing_memory.value
        )  # Get the dictionary containing the UserProfile instance.
        # Format existing music preferences into a string for the prompt.
        formatted_memory = f"Music Preferences: {', '.join(existing_memory_dict.get('memory').music_preferences or [])}"

    # Create a SystemMessage with the formatted prompt, injecting the full conversation history and the existing memory profile.
    formatted_system_message = SystemMessage(
        content=SystemPrompts.memory_creation_prompt().format(
            conversation=state["messages"], memory_profile=formatted_memory
        )
    )

    # Get the Azure OpenAI instance using the singleton pattern
    azure_openai = AzureOpenAI.get_instance(config["settings"])

    # Invoke the LLM with structured output (`UserProfile`) to analyze the conversation and update the memory profile based on new information.
    updated_memory = azure_openai.get_structured_llm(UserProfile).invoke(
        [formatted_system_message]
    )

    # Define the key for storing this specific memory object.
    key = "user_memory"

    # Store the updated memory profile back into the `InMemoryStore`.
    # We wrap `updated_memory` in a dictionary under the key 'memory' for consistency in access.
    store.put(namespace, key, {"memory": updated_memory})

    # Return the updated memory profile.
    return {"loaded_memory": updated_memory}
