# 💸 PONPAY FLASK (Sistem Manajemen Pembayaran & Transaksi)

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey.svg)](https://flask.palletsprojects.com/)

## 📝 Penjelasan Proyek

Proyek **PONPAY FLASK** adalah aplikasi web berbasis Python menggunakan *framework* Flask yang dirancang untuk mengelola berbagai aspek transaksi dan pembayaran. Aplikasi ini bertujuan menyediakan antarmuka terpusat (Dashboard) untuk memantau aktivitas pembayaran, mengelola data pengguna/siswa, dan menyediakan fitur pelaporan data.

### Fitur Utama yang Didukung:

* **Autentikasi Pengguna**: Manajemen login dan sesi.
* **Manajemen Entitas**: Pengelolaan data *Students* (Siswa) dan *Users* (Pengguna/Staf).
* **Transaksi & Pembayaran**: Pencatatan dan pelacakan semua aktivitas pembayaran (*Payments* dan *Transactions*).
* **Pelaporan Data**: Fitur ekspor/impor data menggunakan **Excel (`openpyxl`)** untuk mempermudah audit atau analisis data.
* **Wallet, History, Settings**: Fitur tambahan untuk manajemen saldo, riwayat, dan konfigurasi aplikasi.

---

## ⚙️ Panduan Instalasi dan Menjalankan Proyek (Untuk Pengguna Baru)

Ikuti langkah-langkah ini secara berurutan untuk mengunduh, menyiapkan, dan menjalankan aplikasi Flask di komputer lokal Anda.

### Prasyarat

Pastikan Anda telah menginstal di komputer Anda:
1.  **Python 3.x**
2.  **Git** (untuk mengunduh repositori)

### Langkah 1: Unduh (Clone) Repositori

Buka Terminal (atau Command Prompt/PowerShell) dan *clone* kode dari GitHub:

```bash

git clone https://github.com/kampusriset/23g_flask_pesantren_pay.git
cd 23g_flask_pesantren_pay
```

### Langkah 2: Buat Lingkungan Virtual (Virtual Environment)

Membuat lingkungan virtual mencegah konflik library dengan proyek Python lain di komputer Anda.

### Windows:

```bash

python -m venv venv
.\venv\Scripts\activate
```

### macOS/Linux::

```bash

python3 -m venv venv
source venv/bin/activate
```

Catatan: Setelah diaktifkan, Anda akan melihat (venv) muncul di awal baris Terminal Anda.


### Langkah 3: Instalasi Dependensi Proyek

Instal semua library Python yang dibutuhkan yang tercantum dalam file requirements.txt:


```bash

pip install -r requirements.txt
```

### Langkah 4: Inisialisasi Database

Anda perlu menyiapkan file database awal (jika proyek menggunakan SQLite).


```bash

# Perintah ini akan menjalankan skrip db.py untuk menyiapkan skema database
python db.py
```


### Langkah 5: Jalankan Aplikasi Flask

Setelah semua setup selesai, jalankan file utama aplikasi:


```bash

python app.py
```

### Langkah 6: Akses Aplikasi

- Buka browser web Anda (Chrome, Firefox, dll.).

- Akses alamat: http://127.0.0.1:5000/ atau http://localhost:5000/

- Aplikasi PONPAY FLASK Anda sekarang berjalan dan siap digunakan!

  ### 🗺 Struktur Proyek


```md
  PONPAY FLASK/
├── app.py             # File utama aplikasi Flask
├── routes.py          # Definisi semua rute dan logika terkait
├── db.py              # Skrip/konfigurasi database
├── requirements.txt   # Daftar dependensi Python
├── .gitignore         # File yang dikecualikan dari Git (Wajib ada!)
├── templates/         # Semua file HTML (interface)
└── static/            # File CSS, JavaScript, dan Gambar
```
