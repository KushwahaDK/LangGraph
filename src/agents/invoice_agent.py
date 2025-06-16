"""Invoice information agent for handling billing and invoice queries."""

from ..schemas.state import State
from ..config.prompts import SystemPrompts
from ..tools import get_invoice_tools


class InvoiceAgent:
    """
    Invoice information agent that handles customer billing and invoice queries.

    This agent specializes in retrieving and processing invoice information,
    including customer purchase history and employee assistance details.
    """

    def __init__(self, llm, tools=None):
        """
        Initialize the invoice agent.

        Args:
            llm: Language model instance
            tools: List of invoice-related tools (defaults to INVOICE_TOOLS)
        """
        self.name = "invoice_agent"
        self.description = "Handles invoice and billing information queries"
        self.llm = llm
        self.tools = tools or get_invoice_tools()
        self.invoice_agent = self._create_react_agent()

    def _create_react_agent(self):
        """
        Create a ReAct agent using LangGraph's prebuilt functionality.

        This method demonstrates how to use LangGraph's create_react_agent
        for this invoice agent.

        Returns:
            Compiled LangGraph agent
        """
        from langgraph.prebuilt import create_react_agent

        return create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=SystemPrompts.invoice_assistant_prompt(),
            state_schema=State,
            name=self.name,
        )
