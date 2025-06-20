"""Complete multi-agent workflow with verification, memory management, and human-in-the-loop."""

from typing import Optional
from langchain_openai import AzureChatOpenAI

from langgraph.graph import StateGraph, START, END

from src.schemas.models import UserInput

from ..agents import MusicAgent, InvoiceAgent, SupervisorAgent
from ..schemas.state import State
from ..config.settings import Settings
from ..memory.memory_manager import MemoryManager
from ..utils.database import setup_database
from ..memory.long_term import LongTermMemory
from ..utils.validation import should_interrupt
from ..nodes.verify_info_node import verify_info_node
from ..nodes.human_input_node import human_input_node
from ..tools import get_music_tools, get_invoice_tools


class MultiAgentWorkflow:
    """
    Complete multi-agent workflow implementing the supervisor pattern with:
    - Customer verification
    - Memory management (short-term and long-term)
    - Human-in-the-loop capabilities
    - Specialized sub-agents
    - Tool execution
    """

    def __init__(
        self,
        settings: Optional[Settings] = None,
        memory_manager: Optional[MemoryManager] = None,
    ):
        """
        Initialize the multi-agent workflow.

        Args:
            settings: Application settings
            memory_manager: Memory manager instance
        """
        self.settings = settings

        if memory_manager:
            self.memory_manager = memory_manager
        else:
            self.memory_manager = MemoryManager()

        # Initialize database
        self.db = setup_database()

        # Initialize agents and components
        self._initialize_components()

    def _initialize_components(self):
        """Initialize LLM, agents, and other components."""
        # Initialize LLM
        self._initialize_llm()

        # Initialize agents with appropriate tools
        self._initialize_agents()

    def _initialize_llm(self):
        """Initialize the LLM."""
        self.llm = AzureChatOpenAI(
            model_name=self.settings.model_name,
            temperature=self.settings.temperature,
            api_version=self.settings.api_version,
            api_key=self.settings.azure_openai_api_key,
            azure_endpoint=self.settings.azure_openai_base_url,
        )

        # Initialize structured LLM for parsing
        self.structured_llm = self.llm.with_structured_output(schema=UserInput)

    def _initialize_agents(self):
        """Initialize all agents used in the workflow."""
        # Get tool collections
        self.music_tools = get_music_tools()
        self.invoice_tools = get_invoice_tools()

        # Create specialized agents
        self.music_agent = MusicAgent(self.llm, self.music_tools)
        self.invoice_agent = InvoiceAgent(self.llm, self.invoice_tools)

        # Create supervisor agent with references to specialized agents
        self.supervisor_agent = SupervisorAgent(
            self.llm,
            [self.music_agent, self.invoice_agent],
            self.memory_manager,
        )

    def _configure_workflow_nodes(self, workflow, supervisor_workflow):
        """Configure the nodes of the workflow graph."""
        workflow.add_node("verify_info", verify_info_node)
        workflow.add_node("human_input", human_input_node)
        workflow.add_node("load_memory", LongTermMemory.load_memory)
        workflow.add_node("supervisor", supervisor_workflow)
        workflow.add_node("create_memory", LongTermMemory.save_memory)

    def _configure_workflow_edges(self, workflow):
        """Configure the edges and flow of the workflow graph."""
        # Define the graph's entry point: always start with information verification
        workflow.add_edge(START, "verify_info")

        # Conditional routing after verification
        workflow.add_conditional_edges(
            "verify_info",
            should_interrupt,  # Checks if customer_id is verified
            {
                "continue": "load_memory",  # If verified, proceed to load memory
                "interrupt": "human_input",  # If not verified, get human input
            },
        )

        # Define the rest of the workflow flow
        workflow.add_edge("human_input", "verify_info")
        workflow.add_edge("load_memory", "supervisor")
        workflow.add_edge("supervisor", "create_memory")
        workflow.add_edge("create_memory", END)

    def build_graph(self):
        """
        Create the complete workflow with verification, memory management, and supervision.

        Returns:
            Compiled workflow graph ready for execution
        """
        # Create the main workflow graph
        workflow = StateGraph(State)

        # Get the compiled supervisor workflow (Supervisor + 2 sub-agents graph) from the supervisor agent
        supervisor_workflow = self.supervisor_agent.create_supervisor_workflow()

        # Add nodes to the graph
        self._configure_workflow_nodes(workflow, supervisor_workflow)

        # Define the workflow
        self._configure_workflow_edges(workflow)

        # Compile the final graph with all components
        return workflow.compile(
            name="multi_agent_workflow",
            checkpointer=self.memory_manager.get_checkpointer(),
            store=self.memory_manager.get_store(),
        )
