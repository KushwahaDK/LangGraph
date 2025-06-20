"""Supervisor agent for routing queries to appropriate sub-agents."""

from typing import List

from ..schemas.state import State
from ..config.prompts import SystemPrompts
from ..memory.memory_manager import MemoryManager


class SupervisorAgent:
    """
    Supervisor agent that routes customer queries to appropriate specialized sub-agents.

    This agent acts as a coordinator, analyzing incoming queries and delegating
    them to the most suitable sub-agent based on the query content and context.
    """

    def __init__(self, llm, sub_agents: List, memory_manager):
        """
        Initialize the supervisor agent.

        Args:
            llm: Language model instance for decision making
            sub_agents: List of sub-agents available for delegation
        """
        self.name = "supervisor_agent"
        self.description = "Routes queries to appropriate specialized sub-agents"
        self.llm = llm
        self.tools = []
        self.sub_agents = {agent.name: agent for agent in sub_agents}

        if memory_manager:
            self.memory_manager = memory_manager
        else:
            self.memory_manager = MemoryManager()

    def create_supervisor_workflow(self):
        """Create the supervisor workflow based on the notebook implementation."""
        from langgraph_supervisor import create_supervisor

        # Create supervisor workflow using LangGraph's supervisor pattern
        supervisor_workflow = create_supervisor(
            agents=[
                self.sub_agents["invoice_agent"],
                self.sub_agents["music_agent"],
            ],
            model=self.llm,
            output_mode="last_message",  # Return only the final response
            prompt=SystemPrompts.supervisor_prompt(),  # System instructions for the supervisor agent
            state_schema=State,  # State schema defining data flow structure
            supervisor_name=self.name,
            add_handoff_back_messages=False,  # Add a pair of (AIMessage, ToolMessage) to the message history
        )

        return supervisor_workflow.compile(
            name="supervisor_workflow",
            checkpointer=self.memory_manager.get_checkpointer(),
            store=self.memory_manager.get_store(),
        )

    def visualize_graph(self, workflow_name: str):
        """Visualize the supervisor workflow."""

        from IPython.display import display, Image

        display(Image(workflow_name.get_graph().draw_mermaid_png()))
