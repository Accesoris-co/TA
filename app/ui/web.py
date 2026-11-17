"""
Web UI Interface menggunakan Gradio.
Berjalan sebagai server lokal di USB.
"""
import webbrowser
from threading import Timer

from app.config import AppConfig
from app.history import HistoryManager
from app.inference import InferenceEngine
from app.utils.logger import get_logger

logger = get_logger(__name__)


def create_web_ui(engine: InferenceEngine, config: AppConfig):
    """Buat dan return Gradio interface."""
    try:
        import gradio as gr
    except ImportError:
        raise RuntimeError("Gradio tidak ditemukan di runtime USB.")

    history_manager = HistoryManager(config.db_path)
    session_id = history_manager.new_session()

    def respond(message: str, chat_history: list):
        """Callback untuk setiap pesan dari pengguna."""
        if not message.strip():
            return "", chat_history

        if config.auto_save_history:
            history_manager.add_message(session_id, "user", message)

        chat_history.append((message, ""))
        full_response = ""

        for token in engine.generate(message, stream=True):
            full_response += token
            chat_history[-1] = (message, full_response)
            yield "", chat_history

        if config.auto_save_history and full_response:
            history_manager.add_message(session_id, "assistant", full_response)

    def clear_chat():
        engine.reset_history()
        return []

    with gr.Blocks(
        title="🤖 USB AI System",
        theme=gr.themes.Soft(),
        css=".gradio-container { max-width: 800px !important; margin: auto; }",
    ) as demo:
        gr.Markdown("# 🤖 USB AI System
*Portable AI Assistant — Offline & Bilingual*")

        chatbot = gr.Chatbot(
            height=450,
            label="Percakapan",
            show_label=False,
            bubble_full_width=False,
        )

        with gr.Row():
            msg = gr.Textbox(
                placeholder="Ketik pesan di sini... (Enter untuk kirim)",
                show_label=False,
                scale=4,
            )
            send_btn = gr.Button("Kirim 📤", variant="primary", scale=1)

        with gr.Row():
            clear_btn = gr.Button("🗑️ Hapus Chat", variant="secondary")
            gr.Markdown(
                f"<small>Model: usb-ai-v1 | Port: {config.web_port} | Offline ✅</small>",
                elem_classes="text-right",
            )

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        send_btn.click(respond, [msg, chatbot], [msg, chatbot])
        clear_btn.click(clear_chat, outputs=[chatbot])

    return demo


class WebUI:
    def __init__(self, engine: InferenceEngine, config: AppConfig):
        self.engine = engine
        self.config = config

    def launch(self) -> None:
        """Launch Web UI di browser."""
        demo = create_web_ui(self.engine, self.config)
        url = f"http://localhost:{self.config.web_port}"

        # Buka browser setelah 1.5 detik
        Timer(1.5, lambda: webbrowser.open(url)).start()

        logger.info(f"🌐 Web UI aktif di: {url}")
        demo.launch(
            server_port=self.config.web_port,
            share=False,
            inbrowser=False,
            show_error=True,
        )
