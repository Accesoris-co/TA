@echo off
title USB AI System - Setup
SET USB_ROOT=%~dp0..

echo.
echo  USB AI System - First Time Setup
echo  Memerlukan koneksi internet...
echo.

:: Cek Python sistem untuk setup awal
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [!] Python tidak ditemukan di sistem.
    echo [!] Download dari: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Membuat virtual environment di USB...
python -m venv "%USB_ROOT%\runtime\venv"

echo [2/3] Menginstal dependensi...
"%USB_ROOT%\runtime\venv\Scripts\pip" install --upgrade pip
"%USB_ROOT%\runtime\venv\Scripts\pip" install llama-cpp-python gradio rich click requests

echo [3/3] Membuat direktori data...
mkdir "%USB_ROOT%\data" 2>nul
mkdir "%USB_ROOT%\data\logs" 2>nul
mkdir "%USB_ROOT%\models" 2>nul

echo.
echo [OK] Setup selesai! Jalankan launcher.bat untuk memulai.
echo      Model akan didownload otomatis saat pertama kali dijalankan.
echo.
pause
