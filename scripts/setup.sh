#!/bin/bash
# USB AI System - First Time Setup (Linux/macOS)

USB_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo ""
echo " USB AI System - First Time Setup"
echo " Memerlukan koneksi internet..."
echo ""

# Cek Python
if ! command -v python3 &>/dev/null; then
    echo "[!] Python 3 tidak ditemukan."
    echo "[!] Install: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

echo "[1/3] Membuat virtual environment di USB..."
python3 -m venv "$USB_ROOT/runtime/venv"

echo "[2/3] Menginstal dependensi..."
"$USB_ROOT/runtime/venv/bin/pip" install --upgrade pip
"$USB_ROOT/runtime/venv/bin/pip" install llama-cpp-python gradio rich click requests

echo "[3/3] Membuat direktori data..."
mkdir -p "$USB_ROOT/data/logs"
mkdir -p "$USB_ROOT/models"

chmod +x "$USB_ROOT/scripts/launcher.sh"

echo ""
echo "[OK] Setup selesai! Jalankan ./scripts/launcher.sh untuk memulai."
echo ""
