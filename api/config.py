"""
Configuration management for Emare AI
"""
import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    APP_NAME: str = "Emare AI"
    APP_VERSION: str = "1.0.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8888
    DEBUG: bool = False
    
    # Ollama Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_TIMEOUT: int = 120
    DEFAULT_MODEL: str = "llama3.1:8b"
    
    # Available Models
    AVAILABLE_MODELS: List[str] = [
        "llama3.1:8b",
        "llama3.1:70b",
        "mistral:7b",
        "qwen2.5:7b",
        "gemma2:9b"
    ]
    
    # Security
    API_KEY: str = ""  # Set in .env for production
    CORS_ORIGINS: List[str] = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/emareai.log"
    
    # Performance
    MAX_CONCURRENT_REQUESTS: int = 10
    REQUEST_TIMEOUT: int = 300
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
