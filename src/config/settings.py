"""
Configuration settings for the application.
"""

import os
from pathlib import Path

import yaml


class Config:
    """Load and manage configuration from YAML file."""

    def __init__(self, config_file: str = None):
        """
        Initialize configuration from YAML file.

        Args:
            config_file: Optional path to config file. Defaults to prompts.yaml.
        """
        base_path = Path(__file__).parent
        config_path = (
            base_path / "prompts.yaml"
            if config_file is None
            else Path(config_file)
        )
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def prompt(self, key: str) -> str:
        """
        Retrieve a prompt from configuration.

        Args:
            key: The prompt key.

        Returns:
            The prompt template string.
        """
        return self.config["prompts"][key]


class Settings:
    """Application settings from environment variables."""

    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()

        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
        self.CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
        self.CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "adaptive_rag_documents")


settings = Settings()