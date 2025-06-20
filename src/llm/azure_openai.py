from typing import Type, Dict, Optional
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel
from src.config.settings import Settings


class AzureOpenAI:
    """
    Azure OpenAI client wrapper with singleton pattern to avoid repeated initialization.
    """

    # Class-level dictionary to store instances by settings hash
    _instances: Dict[int, "AzureOpenAI"] = {}

    @classmethod
    def get_instance(cls, settings: Settings) -> "AzureOpenAI":
        """
        Get or create an instance of AzureOpenAI for the given settings.

        Args:
            settings: The settings to use for initialization

        Returns:
            An instance of AzureOpenAI
        """
        # Use settings object id as key to avoid complex hashing
        settings_key = id(settings)

        # If instance doesn't exist for these settings, create it
        if settings_key not in cls._instances:
            cls._instances[settings_key] = cls(settings, _use_singleton=True)

        return cls._instances[settings_key]

    def __init__(self, settings: Settings, _use_singleton: bool = False):
        """
        Initialize the Azure OpenAI client.

        Args:
            settings: The settings to use for initialization
            _use_singleton: Internal parameter to control singleton creation
        """
        if not _use_singleton:
            # Redirect to singleton pattern if not called through get_instance
            raise ValueError(
                "Please use AzureOpenAI.get_instance(settings) to create instances"
            )

        self.settings = settings
        self.llm = None
        self._structured_llms: Dict[str, AzureChatOpenAI] = {}
        self._initialize_llm()

    def _initialize_llm(self):
        """Initialize the LLM."""
        self.llm = AzureChatOpenAI(
            model_name=self.settings.model_name,
            temperature=self.settings.temperature,
            api_version=self.settings.api_version,
            api_key=self.settings.azure_openai_api_key,
            azure_endpoint=self.settings.azure_openai_base_url,
        )

    def get_structured_llm(self, schema: Type[BaseModel]):
        """
        Get the structured LLM for the given schema.
        Caches the structured LLM to avoid repeated initialization.

        Args:
            schema: The schema to use for structured output
        """
        # Use schema name as cache key
        schema_key = schema.__name__

        # Create and cache structured LLM if it doesn't exist
        if schema_key not in self._structured_llms:
            self._structured_llms[schema_key] = self.llm.with_structured_output(
                schema=schema
            )

        return self._structured_llms[schema_key]
