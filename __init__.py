"""
Emare AI - Main Package
Custom AI engine for Emare ecosystem
"""

__version__ = "1.0.0"
__author__ = "Emre"
__description__ = "Emare AI - OpenAI-compatible local inference engine"

from api.config import settings
from inference.ollama_wrapper import OllamaWrapper

__all__ = [
    "settings",
    "OllamaWrapper",
]
