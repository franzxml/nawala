## Fitur
* Halaman utama dengan form upload file PPTX
* Validasi file agar hanya menerima ekstensi `.pptx`
* Konversi PPTX ke PDF menggunakan LibreOffice headless
* Download otomatis file PDF setelah konversi berhasil
* Penyimpanan file sementara di folder `temp`
* Folder kerja unik untuk setiap proses konversi menggunakan UUID
* Deteksi path LibreOffice otomatis untuk macOS, Windows, dan Linux
* Pesan error yang jelas jika file bukan `.pptx`
* Pesan error jika LibreOffice tidak ditemukan
* Pesan error jika proses konversi gagal
* Pesan error jika file PDF hasil konversi tidak terbentuk
* Struktur backend yang modular dan mudah dipahami
* Tampilan HTML dan CSS sederhana, bersih, dan modern

## Teknologi
* Python
* FastAPI
* Uvicorn
* Jinja2
* python-multipart
* LibreOffice headless
* HTML
* CSS
* pathlib
* uuid
* shutil
* subprocess

## Struktur Folder
    nawala/
    │── app/
    │   ├── core/
    │   │   ├── __init__.py
    │   │   └── config.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── converter.py
    │   │   └── libreoffice.py
    │   ├── templates/
    │   │   └── index.html
    │   ├── utils/
    │   │   ├── __init__.py
    │   │   └── files.py
    │   ├── __init__.py
    │   └── main.py
    │── .gitignore
    │── README.md
    └── requirements.txt

## Cara Menjalankan
1. **Persiapan Lingkungan:** Pastikan komputer sudah terinstal **Python**, **pip**, dan **LibreOffice**.

2. **Masuk ke Folder Proyek:**
   ```bash
   cd nawala
   ```

3. **Buat Virtual Environment Opsional:** Langkah ini opsional, tetapi direkomendasikan agar dependensi project terpisah dari Python sistem.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Untuk Windows:
   ```bash
   .venv\Scripts\activate
   ```

4. **Install Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Jalankan Aplikasi:**
   ```bash
   uvicorn app.main:app --reload
   ```

   Jika command `uvicorn` tidak terdeteksi, jalankan dengan:
   ```bash
   python3 -m uvicorn app.main:app --reload
   ```

6. **Akses Aplikasi Lokal:** Buka browser dan kunjungi:
   ```bash
   http://127.0.0.1:8000
   ```

7. **Gunakan Converter:** Upload file `.pptx`, lalu klik tombol **Convert ke PDF**. Jika berhasil, file PDF akan langsung dikirim sebagai download.

## Script
* `pip install -r requirements.txt` untuk menginstall dependensi aplikasi.
* `uvicorn app.main:app --reload` untuk menjalankan aplikasi lokal dengan auto-reload.
* `python3 -m uvicorn app.main:app --reload` sebagai alternatif jika command `uvicorn` tidak tersedia di PATH.
* `python3 -m compileall -q app` untuk mengecek sintaks modul Python di folder `app`.

## Catatan LibreOffice
Aplikasi akan mencoba mendeteksi LibreOffice secara otomatis dari lokasi umum berikut:

* macOS: `/Applications/LibreOffice.app/Contents/MacOS/soffice`
* Windows: `C:\Program Files\LibreOffice\program\soffice.exe`
* Windows: `C:\Program Files (x86)\LibreOffice\program\soffice.exe`
* Linux atau PATH sistem: `libreoffice` atau `soffice`

Jika LibreOffice tidak terdeteksi, install LibreOffice terlebih dahulu. Jika sudah terinstall tetapi tetap tidak terdeteksi, pastikan executable `libreoffice` atau `soffice` tersedia di PATH sistem.

Untuk macOS dengan Homebrew, LibreOffice dapat diinstall menggunakan:
```bash
brew install --cask libreoffice
```

---

Dikembangkan oleh:

* @franzxml