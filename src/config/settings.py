"""Application settings and configuration."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """Application configuration settings."""

    # API Keys
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

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
        if self.openai_api_key:
            os.environ["OPENAI_API_KEY"] = self.openai_api_key
