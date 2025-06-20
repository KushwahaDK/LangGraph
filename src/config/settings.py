"""Application settings and configuration."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """Application configuration settings."""

    # API Keys
    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_openai_base_url: str = os.getenv("AZURE_OPENAI_BASE_URL", "")

    # Model Configuration
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.0
    api_version: str = "2024-08-01-preview"

    # Embedding Configuration
    embedding_model: str = "Alibaba-NLP/gte-modernbert-base"

    # Database Configuration
    database_url: Optional[str] = None

    # Memory Configuration
    memory_store_type: str = "memory"  # Options: "memory", "redis", "postgres"

    def __post_init__(self):
        """Validate and set up environment variables."""
        if self.azure_openai_api_key:
            os.environ["AZURE_OPENAI_API_KEY"] = self.azure_openai_api_key
        if self.azure_openai_base_url:
            os.environ["AZURE_OPENAI_BASE_URL"] = self.azure_openai_base_url
