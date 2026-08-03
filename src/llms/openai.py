"""
OpenAI LLM initialization and configuration.
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from src.config.settings import settings

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

llm = ChatOpenAI(model="gpt-4o-mini")