"""Music catalog agent for handling music-related queries."""

from ..base_agent import BaseAgent
from ...schemas.state import State
from ...config.prompts import SystemPrompts
from ...tools import get_music_tools


class MusicAgent(BaseAgent):
    """
    Music catalog information agent that handles music-related queries.

    This agent specializes in searching for artists, albums, songs, and providing
    music recommendations based on customer preferences.
    """

    def __init__(self, llm, tools=None):
        """
        Initialize the music agent.

        Args:
            llm: Language model instance
            tools: List of music-related tools (defaults to MUSIC_TOOLS)
        """
        super().__init__(
            name="music_catalog_agent",
            description="Handles music catalog queries and recommendations",
            llm=llm,
            tools=tools or get_music_tools(),
        )
        self.music_agent = self._create_react_agent()

    def _create_react_agent(self):
        """
        Create a ReAct agent using LangGraph's prebuilt functionality.
        """
        from langgraph.prebuilt import create_react_agent

        return create_react_agent(
            llm=self.llm,
            tools=self.tools,
            name=self.name,
            state_schema=State,
            prompt=SystemPrompts.music_assistant_prompt(),
        )
