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
        self.chat_provider = "openai"  # informational (openai|deepseek|other compatible)
        # Image provider options (openai | stability)
        self.image_provider = "openai"
        self.stability_api_key = None
        self.stability_engine = "stable-diffusion-v1-6"
        self.stability_base_url = "https://api.stability.ai"

        # Load from config.ini if present
        self._load_from_config()

        # Environment overrides
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AI_API_KEY") or self.api_key
        self.base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("AI_BASE_URL") or self.base_url
        self.chat_model = os.getenv("AI_CHAT_MODEL", self.chat_model)
        self.image_model = os.getenv("AI_IMAGE_MODEL", self.image_model)
        self.chat_provider = os.getenv("AI_CHAT_PROVIDER", self.chat_provider)
        self.image_provider = os.getenv("AI_IMAGE_PROVIDER", self.image_provider)
        self.stability_api_key = os.getenv("STABILITY_API_KEY", self.stability_api_key)
        self.stability_engine = os.getenv("STABILITY_ENGINE", self.stability_engine)
        self.stability_base_url = os.getenv("STABILITY_BASE_URL", self.stability_base_url)

        # Explicit arg overrides
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
                        self.image_provider = cfg.get("AI", "image_provider", fallback=self.image_provider)
                        self.chat_provider = cfg.get("AI", "chat_provider", fallback=self.chat_provider)
                        self.stability_api_key = cfg.get("AI", "stability_api_key", fallback=self.stability_api_key)
                        self.stability_engine = cfg.get("AI", "stability_engine", fallback=self.stability_engine)
                        self.stability_base_url = cfg.get("AI", "stability_base_url", fallback=self.stability_base_url)
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
        # Stability AI branch
        if self.config.image_provider.lower() == "stability":
            api_key = self.config.stability_api_key or self.config.api_key
            if not api_key:
                return None
            # Parse size like "1024x1024"
            try:
                w, h = [int(x) for x in size.lower().split("x")[:2]]
            except Exception:
                w, h = 1024, 1024
            url = f"{self.config.stability_base_url}/v1/generation/{self.config.stability_engine}/text-to-image"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            payload = {
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "height": h,
                "width": w,
                "samples": 1,
            }
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=120)
                resp.raise_for_status()
                data = resp.json()
                arts = data.get("artifacts") or []
                if not arts:
                    return None
                b64 = arts[0].get("base64")
                if not b64:
                    return None
                import base64
                return base64.b64decode(b64)
            except Exception as e:
                print(f"[AI] Stability image error: {e}")
                return None

        # Default: OpenAI-compatible images API
        if not self.config.api_key:
            return None
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
