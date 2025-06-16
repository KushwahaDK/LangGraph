"""Application settings and configuration."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """Application configuration settings."""

    # API Keys
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    langsmith_api_key: str = os.getenv("LANGSMITH_API_KEY", "")
    together_api_key: str = os.getenv("TOGETHER_API_KEY", "")

    # LangSmith Configuration
    langsmith_tracing: str = os.getenv("LANGSMITH_TRACING", "true")
    langsmith_project: str = os.getenv("LANGSMITH_PROJECT", "multi-agent-system")

    # Model Configuration
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.0

    # Embedding Configuration
    embedding_model: str = "Alibaba-NLP/gte-modernbert-base"

    # Database Configuration
    database_url: Optional[str] = None

    # Memory Configuration
    memory_store_type: str = "memory"  # Options: "memory", "redis", "postgres"

    def __post_init__(self):
        """Validate and set up environment variables."""
        if self.langsmith_tracing.lower() == "true":
            os.environ["LANGSMITH_TRACING"] = "true"
            os.environ["LANGSMITH_PROJECT"] = self.langsmith_project
            if self.langsmith_api_key:
                os.environ["LANGSMITH_API_KEY"] = self.langsmith_api_key

        if self.openai_api_key:
            os.environ["OPENAI_API_KEY"] = self.openai_api_key

        if self.together_api_key:
            os.environ["TOGETHER_API_KEY"] = self.together_api_key
