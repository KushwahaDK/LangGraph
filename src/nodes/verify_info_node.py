from src.schemas.state import State
from langchain_core.messages import SystemMessage
from src.utils.database import get_customer_id_from_identifier, setup_database
from langchain_core.runnables import RunnableConfig
from ..config.prompts import SystemPrompts


def verify_info_node(
    state: State,
    config: RunnableConfig,
):
    """
    Verify the customer's account by parsing their input and matching it with the database.

    This node handles customer identity verification as the first step in the support process.
    It extracts customer identifiers (ID, email, or phone) from user messages and validates
    them against the database.

    Args:
        state (State): Current state containing messages and potentially customer_id
        config (RunnableConfig): Configuration for the runnable execution

    Returns:
        dict: Updated state with customer_id if verified, or request for more info
    """
    # Only verify if customer_id is not already set
    if state.get("customer_id") is None:
        # Get the most recent user message
        user_input = state["messages"][-1]

        # Use structured LLM to parse customer identifier from the message
        parsed_info = config["configurable"]["structured_llm"].invoke(
            [SystemMessage(content=SystemPrompts.structured_extraction_prompt())]
            + [user_input]
        )

        # Extract the identifier from parsed response
        identifier = parsed_info.identifier

        # Initialize customer_id as empty
        customer_id = ""

        db = setup_database()
        # Attempt to find the customer ID using the provided identifier
        if identifier:
            customer_id = get_customer_id_from_identifier(identifier, db)

        # If customer found, confirm verification and set customer_id in state
        if customer_id != "":
            intent_message = SystemMessage(
                content=f"Thank you for providing your information! I was able to verify your account with customer id {customer_id}."
            )
            # Note that the return statements only contain keys that are part of the State schema
            return {"customer_id": customer_id, "messages": [intent_message]}
        else:
            llm = config["configurable"]["llm"]
            # If customer not found, ask for correct information
            response = llm.invoke(
                [SystemMessage(content=SystemPrompts.verification_prompt())]
                + state["messages"]
            )
            return {"messages": [response]}

    else:
        # Customer already verified, no action needed
        pass
