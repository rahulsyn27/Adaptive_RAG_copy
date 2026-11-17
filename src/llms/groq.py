"""
Groq LLM initialization and configuration.
"""

import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.config.settings import settings

load_dotenv()
os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=4096
)