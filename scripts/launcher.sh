#!/bin/bash
# USB AI System Launcher — Linux & macOS

USB_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo ""
echo " =========================================="
echo "  USB AI System v1.0.0"
echo "  Portable AI Assistant - Offline Ready"
echo " =========================================="
echo ""

# Cari Python: portable dulu, lalu system
PORTABLE_PY="$USB_ROOT/runtime/python/bin/python3"
if [ -f "$PORTABLE_PY" ]; then
    PYTHON="$PORTABLE_PY"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
    echo "[i] Menggunakan Python sistem: $(python3 --version)"
else
    echo "[!] Python 3 tidak ditemukan."
    echo "[!] Install Python 3.11+ atau jalankan scripts/setup.sh"
    exit 1
fi

# Jalankan aplikasi
"$PYTHON" "$USB_ROOT/app/main.py" "$@"
