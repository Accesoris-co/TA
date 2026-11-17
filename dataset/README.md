# 📊 Dataset Fine-tuning

Direktori ini berisi dataset yang digunakan untuk fine-tuning model AI.

## Struktur

```
dataset/
├── raw/              # Data mentah sebelum preprocessing
├── processed/        # Data yang sudah diproses (format JSONL)
│   ├── train.jsonl   # Data training (80%)
│   ├── val.jsonl     # Data validasi (10%)
│   └── test.jsonl    # Data testing (10%)
└── README.md         # File ini
```

## Format Data

Setiap baris dalam file `.jsonl` mengikuti format ChatML:

```json
{"messages": [
  {"role": "system", "content": "Kamu adalah asisten AI yang membantu."},
  {"role": "user", "content": "Pertanyaan pengguna di sini"},
  {"role": "assistant", "content": "Jawaban AI yang berkualitas di sini"}
]}
```

## Sumber Dataset

| Sumber | Bahasa | Jumlah | Status |
|--------|--------|--------|--------|
| Indonesian Q&A (custom) | ID | TBD | 🔄 Dalam proses |
| General knowledge | ID/EN | TBD | 🔄 Dalam proses |
| Academic domain | ID | TBD | 📋 Direncanakan |

## Cara Menambah Data

1. Tambahkan data mentah ke `raw/`
2. Jalankan script preprocessing (akan dibuat)
3. Verifikasi format dengan validator
4. Gabungkan ke `processed/train.jsonl`

---
*Minimum dataset yang direkomendasikan: 1.000–5.000 pasang percakapan*
