# USB-Embedded Portable AI System

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0--alpha-blue)
![Status](https://img.shields.io/badge/status-in%20development-yellow)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)

**Sistem AI portabel yang tertanam sepenuhnya dalam perangkat USB.**  
*Plug. Run. Intelligence — anywhere, offline.*

</div>

---

## Tentang Proyek

**USB-Embedded Portable AI System** adalah sistem kecerdasan buatan yang sepenuhnya berjalan dari sebuah perangkat USB tanpa memerlukan instalasi apapun di komputer host. Proyek ini merupakan **Tugas Akhir** dalam rangka menyelesaikan Program Studi Informatika di Universitas Andalas.

Sistem ini menggabungkan:
-  **Model AI fine-tuned** (berbasis Qwen2.5 / Phi-3 Mini + QLoRA)
-  **Auto-save & packaging** model langsung ke USB
-  **Runtime portabel** tanpa instalasi (Python Embeddable + llama.cpp)
-  **Antarmuka bilingual** (Indonesia & Inggris) via CLI dan Web UI

---

##  Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
|  **Plug & Play** | Colok USB, jalankan launcher — langsung siap |
|  **Auto-Save Model** | Model diunduh & disimpan otomatis ke USB saat setup pertama |
| **Offline-First** | Tidak membutuhkan koneksi internet untuk inferensi |
|  **Lintas Platform** | Windows, Linux, dan macOS |
|  **Zero Trace** | Tidak ada data yang tertinggal di komputer host |
|  **Riwayat Tersimpan** | Semua percakapan tersimpan di USB (SQLite) |

---

##  Struktur Direktori

```
USB_AI/
├── runtime/              # Portable runtime (Python embeddable / binary)
│   ├── python/
│   └── libs/
├── models/               # Model AI (format GGUF)
│   └── model.gguf
├── app/                  # Kode aplikasi utama
│   ├── main.py
│   ├── inference.py
│   ├── ui_cli.py
│   └── ui_web.py
├── data/                 # Data pengguna (riwayat & konfigurasi)
│   ├── history.db
│   └── config.json
├── scripts/              # Script utilitas
│   ├── setup.bat         # Setup untuk Windows
│   ├── setup.sh          # Setup untuk Linux/macOS
│   ├── launcher.bat
│   └── launcher.sh
├── PRD_USB_AI_System.md  # Product Requirements Document
├── README.md             # Dokumentasi ini
└── LICENSE               # Lisensi proyek
```

---

##  Cara Penggunaan

### Setup Pertama (membutuhkan internet)

**Windows:**
```bat
launcher.bat
```

**Linux / macOS:**
```bash
chmod +x launcher.sh
./launcher.sh
```

> Pada penggunaan pertama, sistem akan otomatis mengunduh model AI (~1–4 GB) dan menyimpannya ke USB. Proses ini hanya dilakukan sekali.

### Penggunaan Normal (offline)

Colok USB ke komputer mana pun dan jalankan launcher. Sistem langsung aktif menggunakan model yang sudah tersimpan di USB — tanpa internet.

---

##  Persyaratan Sistem

| Komponen | Minimum | Rekomendasi |
|----------|---------|-------------|
| RAM | 4 GB | 8 GB |
| CPU | Dual-core x64 | Quad-core x64 |
| Kapasitas USB | 32 GB | 64 GB |
| Kecepatan USB | USB 3.0 | USB 3.1 / 3.2 |
| OS | Windows 10 / Ubuntu 20.04 / macOS 12 | Versi terbaru |

---

##  Stack Teknologi

- **Inference Engine:** [llama.cpp](https://github.com/ggerganov/llama.cpp)
- **Base Model:** Qwen2.5-1.5B / Phi-3 Mini
- **Fine-tuning:** QLoRA via [Unsloth](https://github.com/unslothai/unsloth) di Google Colab
- **Format Model:** GGUF (Q4_K_M quantization)
- **Runtime:** Python 3.11 Embeddable
- **Web UI:** Gradio / Flask
- **Database:** SQLite
- **Bahasa:** Python

---

##  Status Pengembangan

- [x] PRD (Product Requirements Document)
- [ ] Desain Arsitektur Teknis
- [ ] Pemilihan & Persiapan Dataset Fine-tuning
- [ ] Fine-tuning Model (QLoRA)
- [ ] Quantization & Export ke GGUF
- [ ] Implementasi Auto-Save ke USB
- [ ] Portable Runtime Setup
- [ ] CLI Interface
- [ ] Web UI Interface
- [ ] Pengujian Lintas Platform
- [ ] Dokumentasi Laporan TA

---

##  Dokumentasi

- [`PRD_USB_AI_System.md`](./PRD_USB_AI_System.md) — Product Requirements Document

---

##  Penulis

**[Nama Mahasiswa]**
- Program Studi: Informatika
- Universitas: Universitas Andalas
- Tahun: 2026
- Pembimbing: [Nama Dosen Pembimbing]

---

## 📜 Lisensi

Proyek ini dilisensikan di bawah **MIT License** — lihat file [`LICENSE`](./LICENSE) untuk detail lengkapnya.

---

<div align="center">
<i>Dibuat dengan ❤️ sebagai Tugas Akhir — Informatika, Universitas Andalas 2026</i>
</div>

