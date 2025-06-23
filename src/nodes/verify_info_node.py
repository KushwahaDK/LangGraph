from src.llm.azure_openai import AzureOpenAI
from src.schemas.models import UserInput
from src.schemas.state import State
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig
from src.config.prompts import SystemPrompts
from src.databases.database import Database


class VerifyInfoNode:
    """
    Node class for verifying customer account information.

    This node handles customer identity verification as the first step in the support process.
    It extracts customer identifiers (ID, email, or phone) from user messages and validates
    them against the database.
    """

    def __init__(self, db: Database):
        """Initialize the VerifyInfoNode."""
        self.db = db
        self.azure_openai = None
        self.structured_llm = None

    def _initialize_llm(self, config: RunnableConfig):
        """Initialize the Azure OpenAI instance and structured LLM."""
        if self.azure_openai is None:
            self.azure_openai = AzureOpenAI.get_instance(config["settings"])
            self.structured_llm = self.azure_openai.get_structured_llm(UserInput)

    def _parse_customer_identifier(self, user_input) -> str:
        """
        Parse customer identifier from user input using structured LLM.

        Args:
            user_input: The user's message containing potential identifier

        Returns:
            str: The extracted identifier
        """
        parsed_info = self.structured_llm.invoke(
            [SystemMessage(content=SystemPrompts.structured_extraction_prompt())]
            + [user_input]
        )
        return parsed_info.identifier

    def _verify_customer_identity(self, identifier: str):
        """
        Verify customer identity against database.

        Args:
            identifier: Customer identifier (ID, email, or phone)

        Returns:
            Customer ID if found, empty string otherwise
        """
        if identifier:
            return self.db.get_customer_id_from_identifier(identifier)
        return ""

    def _create_verification_success_response(self, customer_id) -> dict:
        """
        Create response for successful customer verification.

        Args:
            customer_id: The verified customer ID

        Returns:
            dict: State update with customer_id and confirmation message
        """
        intent_message = SystemMessage(
            content=f"Thank you for providing your information! I was able to verify your account with customer id {customer_id}."
        )
        return {"customer_id": customer_id, "messages": [intent_message]}

    def _create_verification_failure_response(self, state: State) -> dict:
        """
        Create response for failed customer verification.

        Args:
            state: Current state containing conversation messages

        Returns:
            dict: State update with error message requesting correct information
        """
        response = self.azure_openai.llm.invoke(
            [SystemMessage(content=SystemPrompts.verification_prompt())]
            + state["messages"]
        )
        return {"messages": [response]}

    def execute(self, state: State, config: RunnableConfig) -> dict:
        """
        Verify the customer's account by parsing their input and matching it with the database.

        Args:
            state (State): Current state containing messages and potentially customer_id
            config (RunnableConfig): Configuration for the runnable execution

        Returns:
            dict: Updated state with customer_id if verified, or request for more info
        """
        # Only verify if customer_id is not already set
        if state.get("customer_id") is None:
            # Initialize LLM components
            self._initialize_llm(config)

            # Get the most recent user message
            user_input = state["messages"][-1]

            # Parse customer identifier from the message
            identifier = self._parse_customer_identifier(user_input)

            # Verify customer identity against database
            customer_id = self._verify_customer_identity(identifier)

            # Return appropriate response based on verification result
            if customer_id != "":
                return self._create_verification_success_response(customer_id)
            else:
                return self._create_verification_failure_response(state)
        else:
            # Customer already verified, no action needed
            return {}
