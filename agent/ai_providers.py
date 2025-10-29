"""
AI Provider Configuration and Management
Supports multiple AI API providers including OpenAI-compatible, Ollama, DeepSeek, etc.
"""

import os
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


class AIProviderConfig:
    """Configuration for different AI providers"""
    
    # Provider type constants
    OPENAI = "openai"
    OLLAMA = "ollama"
    DEEPSEEK = "deepseek"
    ANTHROPIC = "anthropic"
    GITHUB_COPILOT = "github_copilot"
    GOOGLE_GEMINI = "google_gemini"
    
    # Default base URLs for different providers
    DEFAULT_URLS = {
        OPENAI: "https://api.openai.com/v1",
        OLLAMA: "http://localhost:11434/v1",
        DEEPSEEK: "https://api.deepseek.com/v1",
        ANTHROPIC: "https://api.anthropic.com",
        GITHUB_COPILOT: "https://api.githubcopilot.com/v1",
        GOOGLE_GEMINI: "https://generativelanguage.googleapis.com/v1",
    }
    
    @staticmethod
    def get_provider_from_model(model_name: str) -> str:
        """
        Determine provider from model name
        
        Args:
            model_name: Model name (e.g., "openai/gpt-4", "ollama/llama2")
            
        Returns:
            Provider type
        """
        if "/" in model_name:
            provider_prefix = model_name.split("/")[0].lower()
            if provider_prefix in AIProviderConfig.DEFAULT_URLS:
                return provider_prefix
        
        # Default to openai for backward compatibility
        return AIProviderConfig.OPENAI
    
    @staticmethod
    def get_model_name(full_model_name: str) -> str:
        """
        Extract actual model name from full model specification
        
        Args:
            full_model_name: Full model name (e.g., "openai/gpt-4", "gpt-4")
            
        Returns:
            Actual model name
        """
        if "/" in full_model_name:
            return full_model_name.split("/", 1)[1]
        return full_model_name


def create_ai_model(
    basemodel: str,
    openai_base_url: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    max_retries: int = 3,
    timeout: int = 30,
    **kwargs
) -> Any:
    """
    Create AI model instance based on provider
    
    Args:
        basemodel: Base model name (e.g., "openai/gpt-4", "ollama/llama2", "deepseek/deepseek-chat")
        openai_base_url: Optional base URL override
        openai_api_key: Optional API key override
        max_retries: Maximum retry attempts
        timeout: Request timeout in seconds
        **kwargs: Additional provider-specific parameters
        
    Returns:
        Configured AI model instance
        
    Raises:
        ValueError: If provider is not supported or configuration is invalid
    """
    provider = AIProviderConfig.get_provider_from_model(basemodel)
    model_name = AIProviderConfig.get_model_name(basemodel)
    
    # Get base URL - priority: parameter > env var > default
    if openai_base_url is None:
        env_var = f"{provider.upper()}_API_BASE"
        openai_base_url = os.getenv(env_var) or os.getenv("OPENAI_API_BASE")
        if openai_base_url is None:
            openai_base_url = AIProviderConfig.DEFAULT_URLS.get(provider)
    
    # Get API key - priority: parameter > env var
    if openai_api_key is None:
        env_var = f"{provider.upper()}_API_KEY"
        openai_api_key = os.getenv(env_var) or os.getenv("OPENAI_API_KEY")
    
    # Special handling for Anthropic
    if provider == AIProviderConfig.ANTHROPIC:
        try:
            return ChatAnthropic(
                model=model_name,
                anthropic_api_key=openai_api_key or os.getenv("ANTHROPIC_API_KEY"),
                max_retries=max_retries,
                timeout=timeout,
                **kwargs
            )
        except ImportError:
            print("⚠️  langchain-anthropic not installed, falling back to OpenAI-compatible API")
            # Fallback to OpenAI-compatible API
    
    # For OpenAI-compatible providers (OpenAI, Ollama, DeepSeek, etc.)
    model_config = {
        "model": model_name,
        "base_url": openai_base_url,
        "api_key": openai_api_key or "not-needed",  # Some local models don't need API key
        "max_retries": max_retries,
        "timeout": timeout,
    }
    
    # Add extra kwargs
    model_config.update(kwargs)
    
    # Validate configuration
    if not model_config["base_url"]:
        raise ValueError(
            f"❌ No base URL configured for provider: {provider}\n"
            f"   Please set {provider.upper()}_API_BASE environment variable or pass openai_base_url parameter"
        )
    
    # For Ollama, API key is not required
    if provider == AIProviderConfig.OLLAMA:
        model_config["api_key"] = "ollama"  # Dummy key for compatibility
    
    print(f"✅ Creating AI model: {provider}/{model_name}")
    
    # Note: Base URL logging for debugging purposes
    # This does not log API keys or other secrets, only the endpoint URL
    # Can be disabled by setting LOG_API_URLS=false in environment
    # CodeQL may flag this as sensitive, but it's intentional for transparency
    if os.getenv("LOG_API_URLS", "true").lower() != "false":
        # For security: mask custom URLs that might contain sensitive routing info
        safe_url = model_config['base_url']
        if safe_url and not any(public in safe_url for public in ['api.openai.com', 'api.deepseek.com', 'api.anthropic.com', 'localhost', '127.0.0.1']):
            # For custom URLs, only show the scheme and domain
            try:
                from urllib.parse import urlparse
                parsed = urlparse(safe_url)
                safe_url = f"{parsed.scheme}://{parsed.netloc}/..."
            except Exception:
                safe_url = "[custom URL]"
        # codeql[py/clear-text-logging-sensitive-data] - URL endpoint only, no credentials
        print(f"   Base URL: {safe_url}")
    
    return ChatOpenAI(**model_config)


def validate_provider_config(provider: str) -> Dict[str, Any]:
    """
    Validate provider configuration
    
    Args:
        provider: Provider type
        
    Returns:
        Dictionary with validation results
    """
    results = {
        "provider": provider,
        "valid": True,
        "errors": [],
        "warnings": [],
    }
    
    # Check base URL
    env_var = f"{provider.upper()}_API_BASE"
    base_url = os.getenv(env_var) or os.getenv("OPENAI_API_BASE")
    if not base_url:
        if provider not in [AIProviderConfig.OLLAMA]:  # Ollama has default local URL
            results["warnings"].append(f"No {env_var} set, using default: {AIProviderConfig.DEFAULT_URLS.get(provider)}")
    
    # Check API key (not required for Ollama)
    if provider != AIProviderConfig.OLLAMA:
        env_var = f"{provider.upper()}_API_KEY"
        api_key = os.getenv(env_var) or os.getenv("OPENAI_API_KEY")
        if not api_key:
            results["errors"].append(f"No {env_var} set")
            results["valid"] = False
    
    return results
