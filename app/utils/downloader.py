"""Downloader model dengan progress bar dan verifikasi checksum."""
import hashlib
import os
from pathlib import Path
from typing import Optional

import requests
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from app.utils.logger import get_logger

logger = get_logger(__name__)


def download_file(
    url: str,
    dest_path: Path,
    expected_sha256: Optional[str] = None,
    chunk_size: int = 8 * 1024 * 1024,  # 8 MB
) -> bool:
    """
    Unduh file dari URL ke dest_path dengan progress bar.
    Verifikasi SHA256 jika expected_sha256 diberikan.
    Returns True jika berhasil.
    """
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = dest_path.with_suffix(".tmp")

    try:
        logger.info(f"Memulai download: {url}")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        sha256 = hashlib.sha256()

        with Progress(
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("📥 Mengunduh model...", total=total_size)

            with open(tmp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        sha256.update(chunk)
                        progress.update(task, advance=len(chunk))

        # Verifikasi checksum
        if expected_sha256:
            actual = sha256.hexdigest()
            if actual.lower() != expected_sha256.lower():
                logger.error(f"Checksum tidak cocok! Expected: {expected_sha256}, Got: {actual}")
                tmp_path.unlink(missing_ok=True)
                return False
            logger.info("✅ Checksum verified.")

        tmp_path.rename(dest_path)
        logger.info(f"✅ Download selesai: {dest_path}")
        return True

    except Exception as e:
        logger.error(f"❌ Download gagal: {e}")
        tmp_path.unlink(missing_ok=True)
        return False
