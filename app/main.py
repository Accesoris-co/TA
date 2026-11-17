"""
Entry point utama USB AI System.
Jalankan via: python app/main.py [--mode cli|web]
"""
import sys
import argparse
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()


def parse_args():
    parser = argparse.ArgumentParser(
        description="USB AI System — Portable AI Assistant"
    )
    parser.add_argument(
        "--mode",
        choices=["cli", "web"],
        default=None,
        help="Mode UI: cli (terminal) atau web (browser). Default dari config.",
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Paksa download ulang model.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Import setelah path siap
    from app.config import load_config, save_config
    from app.model_manager import ModelManager
    from app.inference import InferenceEngine

    console.print(Panel(
        "[bold cyan]🤖 USB AI System[/bold cyan] sedang memulai...",
        border_style="cyan",
    ))

    # 1. Load konfigurasi
    config = load_config()
    if args.mode:
        config.ui_mode = args.mode
        save_config(config)

    # 2. Pastikan model tersedia
    model_manager = ModelManager(config)
    if args.setup or not model_manager.model_exists():
        console.print("[yellow]⚙️  Model belum tersedia, memulai proses setup...[/yellow]")
        if not model_manager.ensure_model_ready():
            console.print("[bold red]❌ Gagal memuat model. Periksa koneksi internet.[/bold red]")
            sys.exit(1)

    # 3. Load inference engine
    console.print("[cyan]🔄 Memuat model ke memori...[/cyan]")
    engine = InferenceEngine(model_manager.get_model_path(), config)
    try:
        engine.load()
    except Exception as e:
        console.print(f"[bold red]❌ Gagal memuat model: {e}[/bold red]")
        sys.exit(1)

    console.print("[bold green]✅ Sistem siap![/bold green]")

    # 4. Jalankan UI sesuai mode
    if config.ui_mode == "web":
        from app.ui.web import WebUI
        WebUI(engine, config).launch()
    else:
        from app.ui.cli import CLI
        CLI(engine, config).run()


if __name__ == "__main__":
    main()
