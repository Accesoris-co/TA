"""
Konfigurasi global sistem USB AI.
Semua path relatif terhadap root USB.
"""
import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path


def get_usb_root() -> Path:
    """Dapatkan root directory USB (parent dari folder app/)."""
    return Path(__file__).resolve().parent.parent


USB_ROOT = get_usb_root()


@dataclass
class ModelConfig:
    path: str = "models/model.gguf"
    context_window: int = 2048
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.95
    repeat_penalty: float = 1.1
    cpu_threads: int = 4


@dataclass
class AppConfig:
    ui_mode: str = "cli"           # "cli" atau "web"
    language: str = "id"           # "id" atau "en"
    web_port: int = 7860
    auto_save_history: bool = True
    system_prompt: str = (
        "Kamu adalah asisten AI yang membantu dan ramah. "
        "Jawab pertanyaan dengan jelas dan informatif dalam Bahasa Indonesia."
    )
    model: ModelConfig = field(default_factory=ModelConfig)

    @property
    def model_path(self) -> Path:
        return USB_ROOT / self.model.path

    @property
    def db_path(self) -> Path:
        return USB_ROOT / "data" / "history.db"

    @property
    def log_path(self) -> Path:
        return USB_ROOT / "data" / "logs" / "app.log"


CONFIG_PATH = USB_ROOT / "data" / "config.json"


def load_config() -> AppConfig:
    """Muat konfigurasi dari config.json, atau buat default jika belum ada."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        model_data = data.pop("model", {})
        return AppConfig(model=ModelConfig(**model_data), **data)
    config = AppConfig()
    save_config(config)
    return config


def save_config(config: AppConfig) -> None:
    """Simpan konfigurasi ke config.json di USB."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = asdict(config)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
