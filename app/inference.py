"""
Inference engine wrapper untuk llama.cpp.
Mendukung streaming dan context management.
"""
from pathlib import Path
from typing import Generator, List, Optional

from app.config import AppConfig
from app.utils.logger import get_logger

logger = get_logger(__name__)


class Message:
    def __init__(self, role: str, content: str):
        self.role = role      # "user", "assistant", "system"
        self.content = content

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}


class InferenceEngine:
    def __init__(self, model_path: Path, config: AppConfig):
        self.model_path = model_path
        self.config = config
        self.llm = None
        self._history: List[Message] = []

    def load(self) -> None:
        """Load model ke memori RAM."""
        try:
            from llama_cpp import Llama
        except ImportError:
            raise RuntimeError(
                "llama-cpp-python tidak ditemukan. "
                "Pastikan runtime USB sudah lengkap."
            )

        logger.info(f"Loading model: {self.model_path}")
        mc = self.config.model
        self.llm = Llama(
            model_path=str(self.model_path),
            n_ctx=mc.context_window,
            n_threads=mc.cpu_threads,
            n_gpu_layers=0,         # CPU-only untuk portabilitas
            verbose=False,
            chat_format="chatml",   # Format untuk Qwen2.5
        )
        logger.info("✅ Model berhasil dimuat.")

    def reset_history(self) -> None:
        """Reset riwayat percakapan sesi ini."""
        self._history = []

    def generate(
        self,
        user_input: str,
        stream: bool = True,
    ) -> Generator[str, None, None]:
        """
        Generate respons AI berdasarkan input pengguna.
        Mendukung streaming output token demi token.
        """
        if self.llm is None:
            raise RuntimeError("Model belum dimuat. Panggil load() terlebih dahulu.")

        # Tambah pesan user ke history
        self._history.append(Message("user", user_input))

        # Bangun messages untuk chat completion
        messages = [{"role": "system", "content": self.config.system_prompt}]
        messages += [m.to_dict() for m in self._history]

        mc = self.config.model
        response = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=mc.max_tokens,
            temperature=mc.temperature,
            top_p=mc.top_p,
            repeat_penalty=mc.repeat_penalty,
            stream=stream,
        )

        full_response = ""
        if stream:
            for chunk in response:
                delta = chunk["choices"][0]["delta"].get("content", "")
                if delta:
                    full_response += delta
                    yield delta
        else:
            full_response = response["choices"][0]["message"]["content"]
            yield full_response

        # Simpan respons ke history
        self._history.append(Message("assistant", full_response))

    def get_history(self) -> List[Message]:
        return self._history
