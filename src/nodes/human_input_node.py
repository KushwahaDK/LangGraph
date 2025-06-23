from langgraph.types import interrupt
from src.schemas.state import State
from langchain_core.runnables import RunnableConfig


class HumanInputNode:
    """
    Node class for handling human input in the workflow.

    This node creates an interruption point in the workflow, allowing the system
    to pause and wait for human input before continuing. It's typically used
    for customer verification or when additional information is needed.
    """

    def __init__(self):
        """Initialize the HumanInputNode."""
        pass

    def execute(self, state: State, config: RunnableConfig):
        """
        Execute the HumanInputNode.

        Returns:
            dict: Updated state with the user's input message
        """
        # Interrupt the workflow and prompt for user input
        user_input = interrupt("Please provide input to verify your identity.")

        # Return the user input as a new message in the state
        return {"messages": [user_input]}
