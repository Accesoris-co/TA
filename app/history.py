"""
Manajemen riwayat percakapan menggunakan SQLite.
Data disimpan sepenuhnya di USB.
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

from app.utils.logger import get_logger

logger = get_logger(__name__)


class HistoryManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        """Inisialisasi skema database."""
        with self._connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                    title       TEXT,
                    model_name  TEXT
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id  INTEGER REFERENCES sessions(id),
                    role        TEXT CHECK(role IN ('user', 'assistant', 'system')),
                    content     TEXT NOT NULL,
                    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
                    tokens_used INTEGER
                );
            """)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def new_session(self, model_name: str = "usb-ai-v1") -> int:
        """Buat sesi percakapan baru. Returns session_id."""
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO sessions (title, model_name) VALUES (?, ?)",
                (f"Sesi {datetime.now().strftime('%d/%m/%Y %H:%M')}", model_name),
            )
            return cur.lastrowid

    def add_message(
        self, session_id: int, role: str, content: str, tokens: int = 0
    ) -> None:
        """Simpan pesan ke database."""
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO messages (session_id, role, content, tokens_used) VALUES (?, ?, ?, ?)",
                (session_id, role, content, tokens),
            )

    def get_sessions(self) -> List[Tuple]:
        """Ambil daftar semua sesi."""
        with self._connect() as conn:
            return conn.execute(
                "SELECT id, created_at, title FROM sessions ORDER BY created_at DESC"
            ).fetchall()

    def get_messages(self, session_id: int) -> List[Tuple]:
        """Ambil semua pesan dalam satu sesi."""
        with self._connect() as conn:
            return conn.execute(
                "SELECT role, content, created_at FROM messages WHERE session_id = ? ORDER BY id",
                (session_id,),
            ).fetchall()
