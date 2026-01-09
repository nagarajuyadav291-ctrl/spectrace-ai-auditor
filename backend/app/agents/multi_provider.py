"""
Multi-Provider AI Executor
Supports: OpenAI, Anthropic, Groq, Google Gemini, Cohere, Hugging Face, Mistral
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from openai import OpenAI
import httpx

class MultiProviderExecutor:
    """Execute AI tasks across multiple providers"""
    
    PROVIDERS = {
        # FREE MODELS
        "llama-3.1-70b-versatile": {"provider": "groq", "free": True},
        "llama-3.1-8b-instant": {"provider": "groq", "free": True},
        "mixtral-8x7b-32768": {"provider": "groq", "free": True},
        "gemini-1.5-flash": {"provider": "google", "free": True},
        "gemini-1.5-pro": {"provider": "google", "free": False},
        "command-r": {"provider": "cohere", "free": True},
        "command-r-plus": {"provider": "cohere", "free": False},
        "mistral-small": {"provider": "mistral", "free": True},
        "mistral-medium": {"provider": "mistral", "free": False},
        
        # PAID MODELS
        "gpt-3.5-turbo": {"provider": "openai", "free": False},
        "gpt-4": {"provider": "openai", "free": False},
        "gpt-4-turbo": {"provider": "openai", "free": False},
        "gpt-4o": {"provider": "openai", "free": False},
        "claude-3-5-sonnet-20241022": {"provider": "anthropic", "free": False},
        "claude-3-opus-20240229": {"provider": "anthropic", "free": False},
        "claude-3-haiku-20240307": {"provider": "anthropic", "free": False},
    }
    
    def __init__(self, model: str):
        self.model = model
        if model not in self.PROVIDERS:
            raise ValueError(f"Unsupported model: {model}")
        
        self.config = self.PROVIDERS[model]
        self.provider = self.config["provider"]
        self._init_client()
    
    def _init_client(self):
        """Initialize the appropriate client"""
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found")
            self.client = OpenAI(api_key=api_key)
            
        elif self.provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found. Get free key at https://console.groq.com")
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            
        elif self.provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found")
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
            
        elif self.provider == "google":
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found. Get free key at https://aistudio.google.com/app/apikey")
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel(self.model)
            
        elif self.provider == "cohere":
            api_key = os.getenv("COHERE_API_KEY")
            if not api_key:
                raise ValueError("COHERE_API_KEY not found. Get free key at https://dashboard.cohere.com/api-keys")
            import cohere
            self.client = cohere.Client(api_key)
            
        elif self.provider == "mistral":
            api_key = os.getenv("MISTRAL_API_KEY")
            if not api_key:
                raise ValueError("MISTRAL_API_KEY not found. Get key at https://console.mistral.ai")
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.mistral.ai/v1"
            )
    
    async def execute(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Execute prompt with selected provider"""
        
        if system_prompt is None:
            system_prompt = "You are a helpful AI assistant. Answer questions clearly and concisely."
        
        try:
            if self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}],
                    system=system_prompt
                )
                return {
                    "response": response.content[0].text,
                    "tokens": response.usage.input_tokens + response.usage.output_tokens,
                    "provider": self.provider,
                    "model": self.model,
                    "success": True
                }
                
            elif self.provider == "google":
                response = self.client.generate_content(prompt)
                return {
                    "response": response.text,
                    "tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0,
                    "provider": self.provider,
                    "model": self.model,
                    "success": True
                }
                
            elif self.provider == "cohere":
                response = self.client.chat(
                    message=prompt,
                    model=self.model,
                    preamble=system_prompt
                )
                return {
                    "response": response.text,
                    "tokens": response.meta.tokens.input_tokens + response.meta.tokens.output_tokens if hasattr(response.meta, 'tokens') else 0,
                    "provider": self.provider,
                    "model": self.model,
                    "success": True
                }
                
            else:  # OpenAI-compatible (OpenAI, Groq, Mistral)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                return {
                    "response": response.choices[0].message.content,
                    "tokens": response.usage.total_tokens if hasattr(response, 'usage') else 0,
                    "provider": self.provider,
                    "model": self.model,
                    "success": True
                }
                
        except Exception as e:
            return {
                "response": None,
                "error": str(e),
                "provider": self.provider,
                "model": self.model,
                "success": False
            }
    
    @classmethod
    def get_available_models(cls) -> Dict[str, List[Dict[str, Any]]]:
        """Get all available models grouped by provider"""
        grouped = {}
        for model, config in cls.PROVIDERS.items():
            provider = config["provider"]
            if provider not in grouped:
                grouped[provider] = []
            grouped[provider].append({
                "model": model,
                "free": config["free"],
                "provider": provider
            })
        return grouped
