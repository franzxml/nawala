## Fitur

- Upload file PPTX dari browser
- Konversi PPTX ke PDF menggunakan LibreOffice secara lokal
- File tidak dikirim ke server eksternal

## Teknologi

- **Runtime:** Python 3.14
- **Backend:** FastAPI, Uvicorn
- **Template engine:** Jinja2
- **Konversi:** LibreOffice (soffice)

## Struktur Folder

```
nawala/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              Konfigurasi path dan konstanta global
│   ├── services/
│   │   ├── __init__.py
│   │   ├── converter.py           Logika konversi PPTX ke PDF via subprocess LibreOffice
│   │   └── libreoffice.py         Deteksi path executable LibreOffice lintas OS
│   ├── templates/
│   │   └── index.html             Halaman utama upload file
│   ├── utils/
│   │   ├── __init__.py
│   │   └── files.py               Helper manajemen file dan temp dir
│   ├── __init__.py
│   └── main.py                    Entry point FastAPI, definisi route
├── tests/
│   ├── __init__.py
│   ├── test_main.py               Test route HTTP
│   ├── test_services_converter.py Test logika konversi
│   └── test_utils_files.py        Test helper file
├── temp/                          Direktori kerja sementara per konversi (dibuat otomatis)
├── .editorconfig
├── .gitignore
├── .vscode/
│   ├── extensions.json            Rekomendasi ekstensi VS Code
│   └── settings.json              Konfigurasi editor (format on save, interpreter path)
├── README.md
├── requirements.txt
└── requirements-dev.txt           Dependency testing (pytest, httpx2)
```

## Cara Menjalankan

**Prasyarat sistem:**
```bash
brew install libreoffice   # macOS
sudo apt install libreoffice   # Ubuntu/Debian
```

1. Clone repositori:
   ```bash
   git clone https://github.com/franzxml/nawala.git && cd nawala
   ```

2. Buat virtual environment dan install dependency:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. Jalankan aplikasi:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Buka browser di `http://localhost:8000`

## Scripts

| Perintah | Keterangan |
|---|---|
| `uvicorn app.main:app --reload` | Jalankan di mode development |
| `uvicorn app.main:app` | Jalankan di mode production |
| `python -m pytest tests/ -v` | Jalankan seluruh test suite |

## Pengembang

- [franzxml](https://github.com/franzxml)
