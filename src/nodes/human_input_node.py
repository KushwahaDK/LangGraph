from langgraph.types import interrupt
from src.schemas.state import State
from langchain_core.runnables import RunnableConfig


def human_input_node(state: State, config: RunnableConfig, prompt: str):
    """
    Human-in-the-loop node that interrupts the workflow to request user input.

    This node creates an interruption point in the workflow, allowing the system
    to pause and wait for human input before continuing. It's typically used
    for customer verification or when additional information is needed.

    Args:
        state (State): Current state containing messages and workflow data
        config (RunnableConfig): Configuration for the runnable execution

    Returns:
        dict: Updated state with the user's input message
    """
    # Interrupt the workflow and prompt for user input
    user_input = interrupt(prompt)

    # Return the user input as a new message in the state
    return {"messages": [user_input]}
