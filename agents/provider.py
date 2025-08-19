"""
Flexible provider configuration for LLM models.
Based on examples/agent/providers.py pattern.
"""
from typing import Optional
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.settings import settings


def get_llm_model(model_choice: Optional[str] = None):
    """
    Get LLM model configuration based on environment variables.
    
    Args:
        model_choice: Optional override for model choice
    
    Returns:
        Configured LLM model client
    """
    llm_choice = model_choice or settings.llm_model
    api_key = settings.llm_api_key
    provider = settings.llm_provider.lower()
    
    # Create provider based on configuration
    if provider == "openai":
        base_url = settings.llm_base_url or "https://api.openai.com/v1"
        return OpenAIChatCompletionClient(
            model=llm_choice,
            api_key=api_key,
            base_url=base_url
        )
    elif provider == "gemini":
        # For Google Gemini, we can use the OpenAI-compatible API endpoint
        # Gemini supports OpenAI-compatible API
        base_url = settings.llm_base_url or "https://generativelanguage.googleapis.com/v1beta"
        return OpenAIChatCompletionClient(
            model=llm_choice,
            api_key=api_key,
            base_url=base_url
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


def get_model_info() -> dict:
    """
    Get information about current model configuration.
    
    Returns:
        Dictionary with model configuration info
    """
    return {
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model,
        "llm_base_url": settings.llm_base_url,
        "app_env": settings.app_env,
        "debug": settings.debug,
    }


def validate_llm_configuration() -> bool:
    """
    Validate that LLM configuration is properly set.
    
    Returns:
        True if configuration is valid
    """
    try:
        # Check if we can create a model instance
        get_llm_model()
        return True
    except Exception as e:
        print(f"LLM configuration validation failed: {e}")
        return False