import os
import logging
from typing import Optional
from .base import AIProvider

logger = logging.getLogger(__name__)

def get_ai_provider(provider_name: Optional[str] = None) -> AIProvider:
    """
    Factory function to get the AI provider based on environment variable or parameter.
    """
    provider_name = provider_name or os.getenv("LLM_PROVIDER", "local").lower()
    
    if provider_name == "vertex":
        from .vertex import VertexAIProvider
        logger.info("Initializing Vertex AI Provider")
        return VertexAIProvider()
    elif provider_name == "openrouter":
        from .openrouter import OpenRouterAIProvider
        logger.info("Initializing OpenRouter AI Provider")
        return OpenRouterAIProvider()
    elif provider_name == "local":
        from .local import LocalAIProvider
        logger.info("Initializing Local AI Provider")
        return LocalAIProvider()
    else:
        logger.warning(f"Unknown provider: {provider_name}. Falling back to 'local'.")
        from .local import LocalAIProvider
        return LocalAIProvider()
