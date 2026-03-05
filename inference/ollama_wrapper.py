"""
Ollama integration wrapper
Handles communication with Ollama server
"""
import httpx
import logging
from typing import List, Dict, Any, AsyncGenerator
import json

logger = logging.getLogger(__name__)


class OllamaWrapper:
    """Wrapper for Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434", timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send chat completion request to Ollama
        
        Args:
            model: Model name (e.g., "llama3.1:8b")
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Max tokens to generate
            stream: Whether to stream response
            
        Returns:
            Response dict from Ollama
        """
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        
        try:
            logger.info(f"Sending chat request to Ollama: model={model}")
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            
            if stream:
                # TODO: Implement streaming
                raise NotImplementedError("Streaming not yet implemented")
            
            result = response.json()
            logger.info(f"Ollama response received: {len(result.get('message', {}).get('content', ''))} chars")
            return result
            
        except httpx.HTTPError as e:
            logger.error(f"Ollama HTTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"Ollama request failed: {e}")
            raise
    
    async def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate completion from prompt
        
        Args:
            model: Model name
            prompt: Text prompt
            temperature: Sampling temperature
            max_tokens: Max tokens to generate
            
        Returns:
            Response dict from Ollama
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            }
        }
        
        try:
            logger.info(f"Sending generate request to Ollama: model={model}")
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"Ollama HTTP error: {e}")
            raise
        except Exception as e:
            logger.error(f"Ollama request failed: {e}")
            raise
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """
        List available models in Ollama
        
        Returns:
            List of model info dicts
        """
        url = f"{self.base_url}/api/tags"
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("models", [])
            
        except httpx.HTTPError as e:
            logger.error(f"Failed to list Ollama models: {e}")
            return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    async def embeddings(self, model: str, prompt: str) -> List[float]:
        """
        Generate embeddings for text
        
        Args:
            model: Embedding model name
            prompt: Text to embed
            
        Returns:
            List of floats (embedding vector)
        """
        url = f"{self.base_url}/api/embeddings"
        
        payload = {
            "model": model,
            "prompt": prompt
        }
        
        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("embedding", [])
            
        except Exception as e:
            logger.error(f"Embeddings request failed: {e}")
            raise
    
    async def health_check(self) -> bool:
        """
        Check if Ollama server is healthy
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
