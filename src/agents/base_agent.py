"""Base agent class for all agents in the multi-agent system."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from langchain_core.runnables import RunnableConfig
from ..schemas.state import State


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the multi-agent system.

    This class defines the common interface that all agents must implement,
    ensuring consistency across different agent types.
    """

    def __init__(self, name: str, description: str, llm=None, tools=None):
        """
        Initialize the base agent.

        Args:
            name (str): Agent identifier name
            description (str): Description of agent capabilities
            llm: Language model instance
            tools: List of tools available to the agent
        """
        self.name = name
        self.description = description
        self.llm = llm
        self.tools = tools or []

    @abstractmethod
    def process(self, state: State, config: RunnableConfig) -> Dict[str, Any]:
        """
        Process the current state and return updated state.

        Args:
            state (State): Current state of the conversation/workflow
            config (RunnableConfig): Configuration for the execution

        Returns:
            Dict[str, Any]: Updated state information
        """
        pass

    def get_tools(self) -> List:
        """
        Get the list of tools available to this agent.

        Returns:
            List: Tools available to the agent
        """
        return self.tools

    def add_tool(self, tool):
        """
        Add a tool to the agent's toolkit.

        Args:
            tool: Tool to add to the agent
        """
        if tool not in self.tools:
            self.tools.append(tool)

    def remove_tool(self, tool):
        """
        Remove a tool from the agent's toolkit.

        Args:
            tool: Tool to remove from the agent
        """
        if tool in self.tools:
            self.tools.remove(tool)

    def get_info(self) -> Dict[str, str]:
        """
        Get basic information about the agent.

        Returns:
            Dict[str, str]: Agent information including name and description
        """
        return {
            "name": self.name,
            "description": self.description,
            "tools_count": len(self.tools),
        }

    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"{self.__class__.__name__}(name='{self.name}', tools={len(self.tools)})"
