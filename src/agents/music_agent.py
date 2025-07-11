"""Music catalog agent for handling music-related queries."""

from src.schemas.state import State
from src.config.prompts import SystemPrompts
from src.tools import get_music_tools


class MusicAgent:
    """
    Music catalog information agent that handles music-related queries.

    This agent specializes in searching for artists, albums, songs, and providing
    music recommendations based on customer preferences.
    """

    def __init__(self, llm, tools=None, db=None):
        """
        Initialize the music agent.

        Args:
            llm: Language model instance
            tools: List of music-related tools (defaults to MUSIC_TOOLS)
        """
        self.name = "music_agent"
        self.description = "Handles music catalog queries and recommendations"
        self.llm = llm
        self.tools = tools or get_music_tools(db)
        self.music_agent = self._create_react_agent()

    def _create_react_agent(self):
        """
        Create a ReAct agent using LangGraph's prebuilt functionality.
        """
        from langgraph.prebuilt import create_react_agent

        return create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=SystemPrompts.music_assistant_prompt(),
            state_schema=State,
            name=self.name,
        )
