"""
Manajemen model AI: pengecekan ketersediaan, download, dan metadata.
"""
import json
from pathlib import Path
from typing import Optional

from app.config import AppConfig, USB_ROOT
from app.utils.checksum import is_valid_model
from app.utils.downloader import download_file
from app.utils.logger import get_logger

logger = get_logger(__name__)

METADATA_PATH = USB_ROOT / "models" / "metadata.json"

# Konfigurasi model default (ganti URL setelah fine-tuning selesai)
DEFAULT_MODEL_INFO = {
    "model_name": "usb-ai-v1",
    "base_model": "Qwen2.5-1.5B-Instruct",
    "fine_tuned": False,
    "quantization": "Q4_K_M",
    "download_url": "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf",
    "sha256": None,  # Isi setelah model tersedia
    "languages": ["id", "en"],
}


class ModelManager:
    def __init__(self, config: AppConfig):
        self.config = config
        self.model_path = config.model_path

    def model_exists(self) -> bool:
        """Cek apakah model sudah ada di USB dan valid."""
        return is_valid_model(self.model_path)

    def get_model_path(self) -> Path:
        return self.model_path

    def get_metadata(self) -> dict:
        if METADATA_PATH.exists():
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return DEFAULT_MODEL_INFO

    def save_metadata(self, info: dict) -> None:
        METADATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(METADATA_PATH, "w", encoding="utf-8") as f:
            json.dump(info, f, indent=2, ensure_ascii=False)

    def download_model(self) -> bool:
        """Unduh model dari URL yang terdaftar di metadata."""
        info = self.get_metadata()
        url = info.get("download_url")
        sha256 = info.get("sha256")

        if not url:
            logger.error("URL download model tidak dikonfigurasi.")
            return False

        logger.info(f"Model tidak ditemukan di USB. Memulai download...")
        logger.info(f"Model: {info.get('model_name')} ({info.get('quantization')})")

        success = download_file(
            url=url,
            dest_path=self.model_path,
            expected_sha256=sha256,
        )

        if success:
            self.save_metadata(info)

        return success

    def ensure_model_ready(self) -> bool:
        """Pastikan model siap digunakan. Download jika belum ada."""
        if self.model_exists():
            logger.info(f"✅ Model ditemukan: {self.model_path}")
            return True

        logger.info("Model belum ada di USB, mencoba download otomatis...")
        return self.download_model()
