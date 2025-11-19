from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QComboBox, QFileDialog
)

try:
    from .client import AIClient, AIConfig
except ImportError:
    # Allow running this file directly: python ai/widgets.py
    from client import AIClient, AIConfig
import configparser, os, requests


class WorkerChat(QThread):
    finished = pyqtSignal(str)

    def __init__(self, client: AIClient, system_prompt: str, user_text: str):
        super().__init__()
        self.client = client
        self.system_prompt = system_prompt
        self.user_text = user_text

    def run(self):
        msg = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self.user_text},
        ]
        text = self.client.chat(msg) or "(No response. Check API key/network.)"
        self.finished.emit(text)


class WorkerImage(QThread):
    finished = pyqtSignal(bytes)

    def __init__(self, client: AIClient, prompt: str):
        super().__init__()
        self.client = client
        self.prompt = prompt

    def run(self):
        data = self.client.generate_image(self.prompt) or b""
        self.finished.emit(data)


class AIChatWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.client = AIClient()

        layout = QVBoxLayout(self)
        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Type your message and press Send...")
        self.send_btn = QPushButton("Send")
        self.system = QLineEdit("You are a helpful assistant living inside CRT Buddy.")
        self.system.setPlaceholderText("System prompt")

        layout.addWidget(QLabel("AI Chat"))
        layout.addWidget(self.history)
        layout.addWidget(QLabel("System"))
        layout.addWidget(self.system)
        row = QHBoxLayout()
        row.addWidget(self.input)
        row.addWidget(self.send_btn)
        layout.addLayout(row)

        self.send_btn.clicked.connect(self.on_send)
        self.input.returnPressed.connect(self.on_send)

    def on_send(self):
        text = self.input.text().strip()
        if not text:
            return
        self.history.append(f"You: {text}")
        self.input.clear()

        self.worker = WorkerChat(self.client, self.system.text(), text)
        self.worker.finished.connect(self.on_reply)
        self.worker.start()

    def on_reply(self, content: str):
        self.history.append(f"AI: {content}")


class AIImageWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.client = AIClient()

        layout = QVBoxLayout(self)
        self.prompt = QTextEdit()
        self.prompt.setPlaceholderText("Describe the image to generate...")
        self.gen_btn = QPushButton("Generate Image")
        self.preview = QLabel("Preview will appear here")
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.save_btn = QPushButton("Save Image")
        self.save_btn.setEnabled(False)
        self._last_image: Optional[bytes] = None

        layout.addWidget(QLabel("AI Image Generator"))
        layout.addWidget(self.prompt)
        layout.addWidget(self.gen_btn)
        layout.addWidget(self.preview, 1)
        layout.addWidget(self.save_btn)

        self.gen_btn.clicked.connect(self.on_generate)
        self.save_btn.clicked.connect(self.on_save)

    def on_generate(self):
        text = self.prompt.toPlainText().strip()
        if not text:
            return
        self.preview.setText("Generating...")
        self.worker = WorkerImage(self.client, text)
        self.worker.finished.connect(self.on_image)
        self.worker.start()

    def on_image(self, data: bytes):
        if not data:
            self.preview.setText("Failed to generate image. Check API key/network.")
            self.save_btn.setEnabled(False)
            return
        self._last_image = data
        pix = QPixmap()
        pix.loadFromData(data)
        self.preview.setPixmap(pix.scaled(512, 512, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.save_btn.setEnabled(True)

    def on_save(self):
        if not self._last_image:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save Image", "ai_image.png", "PNG Files (*.png)")
        if not path:
            return
        try:
            with open(path, "wb") as f:
                f.write(self._last_image)
        except Exception as e:
            self.preview.setText(f"Save failed: {e}")


class TypingGameWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.prompt = QLabel("Press Start to get a typing prompt.")
        self.text = QTextEdit()
        self.text.setPlaceholderText("Type here to match the prompt...")
        self.start_btn = QPushButton("Start")
        self.stats = QLabel("WPM: 0 | Accuracy: 100%")

        layout.addWidget(QLabel("Typing Game"))
        layout.addWidget(self.prompt)
        layout.addWidget(self.text)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stats)

        self.text.textChanged.connect(self.on_type)
        self.start_btn.clicked.connect(self.on_start)
        self._target = ""
        self._start_ts = None

    def on_start(self):
        import random, time
        samples = [
            "HELLO FROM CRT BUDDY",
            "RETRO FUTURE Y2K VIBES",
            "TYPING GAME START NOW",
            "GENERATE COOL MEMES",
        ]
        self._target = random.choice(samples)
        self._start_ts = time.time()
        self.prompt.setText(self._target)
        self.text.clear()
        self.stats.setText("WPM: 0 | Accuracy: 100%")

    def on_type(self):
        import time
        if not self._target or self._start_ts is None:
            return
        typed = self.text.toPlainText()
        elapsed = max(1e-6, time.time() - self._start_ts)
        # WPM: characters/5 per minute
        wpm = (len(typed) / 5.0) / (elapsed / 60.0)
        # Accuracy
        correct = sum(1 for a, b in zip(typed, self._target) if a == b)
        acc = 100.0 * (correct / max(1, len(typed)))
        self.stats.setText(f"WPM: {int(wpm)} | Accuracy: {int(acc)}%")


class AISettingsWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Core settings
        self.api_key = QLineEdit()
        self.base_url = QLineEdit()
        self.base_url_preset = QComboBox()
        self.base_url_preset.addItems(["custom", "openai", "deepseek"])
        self.chat_model = QLineEdit("gpt-4o-mini")
        self.image_model = QLineEdit("gpt-image-1")

        # Chat provider (openai | deepseek)
        self.chat_provider = QComboBox()
        self.chat_provider.addItems(["openai", "deepseek"])

        # Image provider (openai | stability)
        self.image_provider = QComboBox()
        self.image_provider.addItems(["openai", "stability"])

        # Stability fields
        self.stability_api_key = QLineEdit()
        self.stability_base_url = QLineEdit("https://api.stability.ai")
        self.stability_engine = QLineEdit("stable-diffusion-v1-6")

        # Buttons & status
        self.save_btn = QPushButton("Save Settings")
        self.test_btn = QPushButton("Test Connection")
        self.status = QLabel("")

        # Layout wiring
        layout.addWidget(QLabel("API Key"))
        layout.addWidget(self.api_key)
        layout.addWidget(QLabel("Base URL (OpenAI-compatible)"))
        layout.addWidget(self.base_url)
        layout.addWidget(QLabel("Base URL Preset"))
        layout.addWidget(self.base_url_preset)
        layout.addWidget(QLabel("Chat Provider"))
        layout.addWidget(self.chat_provider)
        layout.addWidget(QLabel("Chat Model"))
        layout.addWidget(self.chat_model)
        layout.addWidget(QLabel("Image Provider"))
        layout.addWidget(self.image_provider)
        layout.addWidget(QLabel("Image Model"))
        layout.addWidget(self.image_model)
        layout.addWidget(QLabel("Stability API Key"))
        layout.addWidget(self.stability_api_key)
        layout.addWidget(QLabel("Stability Base URL"))
        layout.addWidget(self.stability_base_url)
        layout.addWidget(QLabel("Stability Engine"))
        layout.addWidget(self.stability_engine)
        row = QHBoxLayout()
        row.addWidget(self.save_btn)
        row.addWidget(self.test_btn)
        layout.addLayout(row)
        layout.addWidget(self.status)

        # Signals
        self.save_btn.clicked.connect(self.on_save)
        self.test_btn.clicked.connect(self.on_test)
        self.image_provider.currentTextChanged.connect(self._toggle_provider_fields)
        self.chat_provider.currentTextChanged.connect(self._apply_chat_provider_defaults)
        self.base_url_preset.currentTextChanged.connect(self._on_base_url_preset_changed)
        self.base_url.textChanged.connect(self._on_base_url_text_changed)

        # Init
        self._load()
        self._toggle_provider_fields(self.image_provider.currentText())
        self._apply_chat_provider_defaults(self.chat_provider.currentText())
        self._sync_preset_with_base_url()

    def _cfg_path(self) -> str:
        # write into CRT_Buddy/config.ini
        here = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        cfg = os.path.join(here, "config.ini")
        if not os.path.exists(cfg):
            # fallback to project root if needed
            cfg = os.path.join(os.path.dirname(here), "config.ini")
        return cfg

    def _load(self):
        cfg = configparser.ConfigParser()
        try:
            cfg.read(self._cfg_path(), encoding="utf-8")
            if cfg.has_section("AI"):
                self.api_key.setText(cfg.get("AI", "api_key", fallback=""))
                self.base_url.setText(cfg.get("AI", "base_url", fallback=""))
                self.chat_model.setText(cfg.get("AI", "chat_model", fallback=self.chat_model.text()))
                self.image_model.setText(cfg.get("AI", "image_model", fallback=self.image_model.text()))
                self.image_provider.setCurrentText(cfg.get("AI", "image_provider", fallback="openai"))
                self.chat_provider.setCurrentText(cfg.get("AI", "chat_provider", fallback=self.chat_provider.currentText()))
                self.base_url_preset.setCurrentText(cfg.get("AI", "base_url_preset", fallback=self.base_url_preset.currentText()))
                self.stability_api_key.setText(cfg.get("AI", "stability_api_key", fallback=""))
                self.stability_base_url.setText(cfg.get("AI", "stability_base_url", fallback=self.stability_base_url.text()))
                self.stability_engine.setText(cfg.get("AI", "stability_engine", fallback=self.stability_engine.text()))
        except Exception:
            pass

    def on_save(self):
        cfg = configparser.ConfigParser()
        path = self._cfg_path()
        try:
            cfg.read(path, encoding="utf-8")
        except Exception:
            pass
        if not cfg.has_section("AI"):
            cfg.add_section("AI")
        cfg.set("AI", "api_key", self.api_key.text().strip())
        cfg.set("AI", "base_url", self.base_url.text().strip())
        cfg.set("AI", "chat_model", self.chat_model.text().strip())
        cfg.set("AI", "image_model", self.image_model.text().strip())
        cfg.set("AI", "image_provider", self.image_provider.currentText().strip())
        cfg.set("AI", "chat_provider", self.chat_provider.currentText().strip())
        cfg.set("AI", "base_url_preset", self.base_url_preset.currentText().strip())
        cfg.set("AI", "stability_api_key", self.stability_api_key.text().strip())
        cfg.set("AI", "stability_base_url", self.stability_base_url.text().strip())
        cfg.set("AI", "stability_engine", self.stability_engine.text().strip())
        with open(path, "w", encoding="utf-8") as f:
            cfg.write(f)
        self.status.setText(f"Saved to {path}")

    def on_test(self):
        provider = self.image_provider.currentText().strip().lower()
        self.status.setText("Testing...")
        if provider == "stability":
            key = (self.stability_api_key.text().strip() or self.api_key.text().strip())
            base = self.stability_base_url.text().strip().rstrip("/") or "https://api.stability.ai"
            if not key:
                self.status.setText("Enter Stability API Key.")
                return
            try:
                resp = requests.get(f"{base}/v1/engines/list", headers={"Authorization": f"Bearer {key}"}, timeout=15)
                if resp.status_code == 200:
                    try:
                        js = resp.json()
                        count = len(js) if isinstance(js, list) else len(js.get("engines", []))
                        self.status.setText(f"Success: reachable (engines: {count})")
                    except Exception:
                        self.status.setText("Success: HTTP 200")
                elif resp.status_code == 401:
                    self.status.setText("Unauthorized (401): API key invalid or lacks access.")
                elif resp.status_code == 403:
                    self.status.setText("Forbidden (403): Check account/permissions.")
                elif resp.status_code == 404:
                    self.status.setText("Not Found (404): Check Base URL.")
                else:
                    self.status.setText(f"HTTP {resp.status_code}: {resp.text[:120]}")
            except requests.exceptions.RequestException as e:
                self.status.setText(f"Network error: {e}")
        else:
            key = self.api_key.text().strip()
            base = self.base_url.text().strip().rstrip("/") or "https://api.openai.com/v1"
            if not key:
                self.status.setText("Please enter API Key first.")
                return
            try:
                resp = requests.get(f"{base}/models", headers={"Authorization": f"Bearer {key}"}, timeout=15)
                if resp.status_code == 200:
                    try:
                        js = resp.json()
                        count = len(js.get("data", []))
                        self.status.setText(f"Success: reachable (models: {count})")
                    except Exception:
                        self.status.setText("Success: HTTP 200")
                elif resp.status_code == 401:
                    self.status.setText("Unauthorized (401): API key invalid or lacks access.")
                elif resp.status_code == 403:
                    self.status.setText("Forbidden (403): Check account/permissions.")
                elif resp.status_code == 404:
                    self.status.setText("Not Found (404): Check Base URL.")
                else:
                    self.status.setText(f"HTTP {resp.status_code}: {resp.text[:120]}")
            except requests.exceptions.RequestException as e:
                self.status.setText(f"Network error: {e}")

    def _toggle_provider_fields(self, provider: str):
        p = provider.strip().lower()
        is_stability = p == "stability"
        # For usability, show Stability fields only when needed
        self.stability_api_key.setEnabled(is_stability)
        self.stability_base_url.setEnabled(is_stability)
        self.stability_engine.setEnabled(is_stability)

    def _apply_chat_provider_defaults(self, provider: str):
        p = provider.strip().lower()
        if p == "deepseek":
            # Only set if user hasn't customized
            if not self.base_url.text().strip():
                self.base_url.setText("https://api.deepseek.com/v1")
            if self.chat_model.text().strip() in ("", "gpt-4o-mini", "gpt-4", "gpt-4o", "gpt-3.5-turbo"):
                self.chat_model.setText("deepseek-chat")
            self.base_url_preset.setCurrentText("deepseek")
        else:  # openai default
            if not self.base_url.text().strip() or "deepseek" in self.base_url.text():
                self.base_url.setText("https://api.openai.com/v1")
            if self.chat_model.text().strip() == "deepseek-chat":
                self.chat_model.setText("gpt-4o-mini")
            self.base_url_preset.setCurrentText("openai")
        self._sync_preset_with_base_url()

    def _on_base_url_preset_changed(self, preset: str):
        p = preset.strip().lower()
        if p == "openai":
            self.base_url.setText("https://api.openai.com/v1")
            if self.chat_provider.currentText().lower() == "openai" and self.chat_model.text().strip() == "deepseek-chat":
                self.chat_model.setText("gpt-4o-mini")
        elif p == "deepseek":
            self.base_url.setText("https://api.deepseek.com/v1")
            if self.chat_provider.currentText().lower() == "deepseek" and self.chat_model.text().strip() in ("", "gpt-4o-mini", "gpt-4", "gpt-4o", "gpt-3.5-turbo"):
                self.chat_model.setText("deepseek-chat")
        # custom: do nothing
        self._sync_preset_with_base_url()

    def _on_base_url_text_changed(self, _text: str):
        # If user edits base_url manually, sync preset to custom unless exact match
        self._sync_preset_with_base_url()

    def _sync_preset_with_base_url(self):
        url = self.base_url.text().strip().rstrip("/")
        if url == "https://api.openai.com/v1":
            if self.base_url_preset.currentText() != "openai":
                self.base_url_preset.setCurrentText("openai")
        elif url == "https://api.deepseek.com/v1":
            if self.base_url_preset.currentText() != "deepseek":
                self.base_url_preset.setCurrentText("deepseek")
        else:
            if self.base_url_preset.currentText() != "custom":
                self.base_url_preset.setCurrentText("custom")


if __name__ == "__main__":
    # Minimal launcher to test Settings UI directly
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = AISettingsWidget()
    w.setWindowTitle("CRT Buddy - AI Settings Test")
    w.resize(500, 360)
    w.show()
    sys.exit(app.exec())
