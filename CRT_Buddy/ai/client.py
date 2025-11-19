import os
import configparser
from typing import List, Optional

import requests


class AIConfig:
    """Configuration for AI API access."""

    def __init__(self,
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 chat_model: str = "gpt-4o-mini",
                 image_model: str = "gpt-image-1"):
        # Defaults
        self.api_key = None
        self.base_url = "https://api.openai.com/v1"
        self.chat_model = chat_model
        self.image_model = image_model

        # Load from config.ini if present
        self._load_from_config()

        # Override from environment
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AI_API_KEY") or self.api_key
        self.base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("AI_BASE_URL") or self.base_url
        self.chat_model = os.getenv("AI_CHAT_MODEL", self.chat_model)
        self.image_model = os.getenv("AI_IMAGE_MODEL", self.image_model)

        # Override from explicit args last (highest precedence)
        if api_key:
            self.api_key = api_key
        if base_url:
            self.base_url = base_url

    def _load_from_config(self):
        cfg = configparser.ConfigParser()
        cfg_path_candidates = [
            os.path.join(os.path.dirname(__file__), "..", "config.ini"),
            os.path.join(os.path.dirname(__file__), "..", "..", "config.ini"),
            os.path.join(os.getcwd(), "CRT_Buddy", "config.ini"),
            os.path.join(os.getcwd(), "config.ini"),
        ]
        for p in cfg_path_candidates:
            p = os.path.abspath(p)
            if os.path.exists(p):
                try:
                    cfg.read(p, encoding="utf-8")
                    if cfg.has_section("AI"):
                        self.api_key = cfg.get("AI", "api_key", fallback=self.api_key)
                        self.base_url = cfg.get("AI", "base_url", fallback=self.base_url) or self.base_url
                        self.chat_model = cfg.get("AI", "chat_model", fallback=self.chat_model)
                        self.image_model = cfg.get("AI", "image_model", fallback=self.image_model)
                    break
                except Exception:
                    # Ignore parse errors and continue
                    pass


class AIClient:
    """Minimal OpenAI-compatible client for chat and image generation.

    Supports OpenAI or any OpenAI-compatible server by customizing base_url.
    """

    def __init__(self, config: Optional[AIConfig] = None):
        self.config = config or AIConfig()
        if not self.config.api_key:
            # Allow running without key; callers should handle None outputs gracefully
            print("[AI] Warning: No API key set. Set OPENAI_API_KEY or AI_API_KEY.")

    # --------- Chat Completion ---------
    def chat(self, messages: List[dict], model: Optional[str] = None, temperature: float = 0.7, max_tokens: int = 512) -> Optional[str]:
        if not self.config.api_key:
            return None
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model or self.config.chat_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content")
        except Exception as e:
            print(f"[AI] Chat error: {e}")
            return None

    # --------- Image Generation ---------
    def generate_image(self, prompt: str, model: Optional[str] = None, size: str = "1024x1024") -> Optional[bytes]:
        if not self.config.api_key:
            return None
        # OpenAI image generation endpoint (DALL·E-style)
        url = f"{self.config.base_url}/images/generations"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model or self.config.image_model,
            "prompt": prompt,
            "size": size,
            "response_format": "b64_json",
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()
            b64 = data.get("data", [{}])[0].get("b64_json")
            if not b64:
                return None
            import base64
            return base64.b64decode(b64)
        except Exception as e:
            print(f"[AI] Image error: {e}")
            return None
