# 💸 PonPay - Sistem Pembayaran Pondok Pesantren Al Huda

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey.svg)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-orange.svg)](https://www.mysql.com/)

**PonPay** adalah aplikasi web manajemen keuangan dan pembayaran yang dirancang khusus untuk Pondok Pesantren Al Huda. Aplikasi ini memudahkan pengelolaan data santri, pencatatan transaksi (pemasukan & pengeluaran), pemantauan tunggakan SPP/tagihan, serta pelaporan keuangan yang transparan dan akuntabel.

---
## Flowchart
![WhatsApp Image 2026-02-03 at 15 16 57](https://github.com/user-attachments/assets/073eaef9-17a6-40e2-851a-daf3d699aa36)

## Nama Tim
1. Luky Susanto : logika aplikasi, kemudahan pemakaian dan desain awal
2. Azmi Adam M : Pengembangan UI/UX utama, integrasi frontend dengan backend, serta pengelolaan struktur halaman
3. Dikry Aljanata : penambah fitur, perbaikan bug
4. Irwan Wahyu W : Perbaikan toogle sidebar dan Tampilan profile
5. Bintang Aulia : menambahkan tampilan halaman login

## Link Video Dokumentasi
Anda dapat menonton video dokumentasi aplikasi melalui tautan berikut:https://bit.ly/KLIKSINIDONG

## ✨ Fitur Utama

### 📊 Dashboard & Statistik

- **Ringkasan Real-time**: Menampilkan total pemasukan, pengeluaran, saldo saat ini, dan jumlah transaksi bulanan.
- **Visualisasi Data**: Grafik interaktif (Chart.js) untuk tren keuangan, klasifikasi pengeluaran vs pemasukan, dan statistik tunggakan per kelas.

### 👥 Manajemen Santri (Siswa)

- **Data Lengkap**: Pengelolaan biodata santri (CRUD), termasuk foto profil, data wali, dan status aktif/non-aktif.
- **Riwayat Pembayaran**: Memantau history pembayaran spesifik untuk setiap santri.

### 💰 Transaksi & Keuangan

- **Pencatatan Transaksi**: Input pemasukan (SPP, donasi, dll) dan pengeluaran (operasional, gaji, dll).
- **Kwitansi Digital**: Cetak bukti pembayaran (Kwitansi) dalam format **PDF** secara otomatis.
- **Dompet Pondok**: Pemantauan saldo kas pondok secara real-time.

### 🧾 Tagihan & Tunggakan

- **Manajemen Tagihan**: Buat tagihan bulanan atau insidentil untuk santri.
- **Monitoring Tunggakan**: Laporan otomatis jumlah santri yang belum lunas dan total nominal tunggakan per kelas.

### 🔐 Keamanan & Akses

- **Role-Based Access Control (RBAC)**:
  - **Admin**: Akses penuh (termasuk manajemen user dan hapus data).
  - **Staff/Bendahara**: Akses terbatas (input transaksi, lihat data, cetak kwitansi).
- **CSRF Protection**: Perlindungan formulir dari serangan Cross-Site Request Forgery.
- **Secure Login**: Sistem autentikasi aman dengan hashing password.

### 📝 Laporan & Audit

- **Audit Log (Riwayat)**: Mencatat setiap aktivitas user (siapa mengubah apa) untuk transparansi.
- **Ekspor Data**: Unduh laporan transaksi dalam format Excel.

---

## 🛠️ Teknologi yang Digunakan

- **Backend**: Python (Flask Framework)
- **Database**: MySQL (via `mysql-connector-python`)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Visualisasi**: Chart.js
- **PDF Generator**: FPDF2
- **Form Security**: Flask-WTF

---

## ⚙️ Panduan Instalasi & Menjalankan Aplikasi

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer lokal (Windows/Linux/Mac).

### Prasyarat

1.  **Python 3.8+** terinstal.
2.  **XAMPP** (atau server MySQL lainnya) terinstal dan berjalan.
3.  **Git** terinstal.

### 1. Clone Repositori

```bash
git clone https://github.com/kampusriset/23g_flask_pesantren_pay.git
cd 23g_flask_pesantren_pay
```

### 2. Buat Virtual Environment (Disarankan)

Mengisolasi dependensi proyek agar tidak bentrok dengan sistem.

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instal Dependensi

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Database

1.  Pastikan **MySQL** di XAMPP sudah berjalan (Klik **Start** pada modul MySQL).
2.  Buat database baru bernama `ponpay` (opsional, aplikasi akan mencoba membuatnya otomatis, tapi lebih baik dibuat manual di phpMyAdmin jika gagal).
3.  Cek koneksi di file `app.py` (Default XAMPP):
    ```python
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''  # Password default XAMPP biasanya kosong
    app.config['MYSQL_DB'] = 'ponpay'
    ```

### 5. Jalankan Aplikasi

Aplikasi akan otomatis membuat tabel-tabel yang dibutuhkan saat pertama kali dijalankan.

```bash
python app.py
```

_Tunggu hingga muncul pesan `Running on http://127.0.0.1:5000`_

### 6. Login

Buka browser dan akses **http://127.0.0.1:5000**.
Gunakan akun default administrator:

- **Username**: `admin`
- **Password**: `admin123`

_(Jangan lupa ganti password setelah login pertama kali!)_

---

## � Struktur Proyek

```
PONPAY/
├── app.py              # Entry point aplikasi & konfigurasi global
├── routes.py           # Logic routing & controller
├── db.py               # Koneksi database & schema creation
├── requirements.txt    # Daftar library Python
├── templates/          # File HTML (Jinja2)
│   ├── base.html       # Layout utama
│   ├── dashboard.html  # Halaman utama
│   ├── transaction.html
│   └── ...
├── static/             # Aset statis (CSS, JS, Images)
└── ...
```

---

## 👨‍💻 Kontribusi & Lisensi

Dikembangkan oleh Tim IT Pondok Pesantren Al Huda.
Hak Cipta © 2025.
