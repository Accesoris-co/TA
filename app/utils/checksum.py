"""Verifikasi integritas file menggunakan SHA256."""
import hashlib
from pathlib import Path
from typing import Optional


def compute_sha256(file_path: Path, chunk_size: int = 8 * 1024 * 1024) -> str:
    """Hitung SHA256 checksum dari sebuah file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)
    return sha256.hexdigest()


def verify_checksum(file_path: Path, expected: str) -> bool:
    """Verifikasi apakah file cocok dengan checksum yang diharapkan."""
    actual = compute_sha256(file_path)
    return actual.lower() == expected.lower()


def is_valid_model(file_path: Path, expected_sha256: Optional[str] = None) -> bool:
    """Cek apakah file model valid (ada dan ukurannya masuk akal)."""
    if not file_path.exists():
        return False
    if file_path.stat().st_size < 100 * 1024 * 1024:  # minimal 100MB
        return False
    if expected_sha256:
        return verify_checksum(file_path, expected_sha256)
    return True
