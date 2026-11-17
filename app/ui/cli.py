"""
CLI Interface untuk USB AI System.
Interaksi langsung via terminal dengan dukungan streaming.
"""
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from app.config import AppConfig
from app.history import HistoryManager
from app.inference import InferenceEngine
from app.utils.logger import get_logger

logger = get_logger(__name__)
console = Console()

COMMANDS = {
    "/help":    "Tampilkan bantuan",
    "/clear":   "Bersihkan layar & mulai sesi baru",
    "/history": "Tampilkan daftar sesi sebelumnya",
    "/exit":    "Keluar dari aplikasi",
}


class CLI:
    def __init__(self, engine: InferenceEngine, config: AppConfig):
        self.engine = engine
        self.config = config
        self.history = HistoryManager(config.db_path)
        self.session_id = self.history.new_session()

    def _print_banner(self) -> None:
        console.print(Panel(
            "[bold cyan]🤖 USB AI System v1.0.0[/bold cyan]
"
            "[dim]Model: usb-ai-v1 | Offline | Bilingual ID/EN[/dim]
"
            "[dim]Ketik [bold]/help[/bold] untuk daftar perintah[/dim]",
            border_style="cyan",
        ))

    def _handle_command(self, cmd: str) -> bool:
        """Handle perintah khusus. Returns False jika /exit."""
        if cmd == "/help":
            console.print(Panel(
                "\n".join(f"[bold]{k}[/bold] — {v}" for k, v in COMMANDS.items()),
                title="Perintah Tersedia",
                border_style="green",
            ))
        elif cmd == "/clear":
            console.clear()
            self.engine.reset_history()
            self.session_id = self.history.new_session()
            self._print_banner()
        elif cmd == "/history":
            sessions = self.history.get_sessions()
            if sessions:
                for sid, created, title in sessions:
                    console.print(f"  [{sid}] {created} — {title}")
            else:
                console.print("[dim]Belum ada riwayat.[/dim]")
        elif cmd == "/exit":
            console.print("[bold red]👋 Sampai jumpa![/bold red]")
            return False
        return True

    def run(self) -> None:
        """Jalankan loop interaktif CLI."""
        console.clear()
        self._print_banner()

        while True:
            try:
                user_input = Prompt.ask("\n[bold green]You[/bold green]").strip()
            except (KeyboardInterrupt, EOFError):
                console.print("\n[bold red]👋 Keluar...[/bold red]")
                break

            if not user_input:
                continue

            if user_input.startswith("/"):
                if not self._handle_command(user_input):
                    break
                continue

            # Simpan pesan user
            if self.config.auto_save_history:
                self.history.add_message(self.session_id, "user", user_input)

            # Generate & stream respons
            console.print("\n[bold blue]AI[/bold blue]", end=" ")
            full_response = ""
            try:
                for token in self.engine.generate(user_input, stream=True):
                    console.print(token, end="", highlight=False)
                    full_response += token
                console.print()  # newline setelah streaming selesai
            except Exception as e:
                console.print(f"[bold red]Error: {e}[/bold red]")
                logger.error(f"Inference error: {e}")
                continue

            # Simpan respons AI
            if self.config.auto_save_history and full_response:
                self.history.add_message(self.session_id, "assistant", full_response)
