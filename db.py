"""
Database Configuration dan Management (MySQL Version)
"""
import mysql.connector
from mysql.connector import Error
from flask import g, current_app
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash, check_password_hash

def get_db():
    """Mendapatkan koneksi database"""
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DB']
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    return g.db

def close_db(e=None):
    """Menutup koneksi database"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Inisialisasi database dengan schema"""
    # Create database if not exists
    try:
        conn = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {current_app.config['MYSQL_DB']}")
        conn.close()
    except Error as e:
        print(f"Error creating database: {e}")
        return

    db = get_db()
    c = db.cursor()
    
    # Tabel Users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(255),
        full_name VARCHAR(255),
        role VARCHAR(50) DEFAULT 'user',
        profile_picture VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Tabel Students (Santri)
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        nisn VARCHAR(50) UNIQUE,
        kelas VARCHAR(50),
        jenis_kelamin VARCHAR(20),
        phone VARCHAR(20),
        parent_name VARCHAR(255),
        parent_phone VARCHAR(20),
        alamat TEXT,
        status VARCHAR(20) DEFAULT 'aktif',
        photo VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Tabel Transactions
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        student_id INT,
        type VARCHAR(50) NOT NULL,
        category VARCHAR(100) NOT NULL,
        amount INT NOT NULL,
        description TEXT,
        date DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (student_id) REFERENCES students(id)
    )''')
    
    # Tabel Wallet (Saldo Pondok)
    c.execute('''CREATE TABLE IF NOT EXISTS wallet (
        id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        balance INT DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # Tabel Settings
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
        id INT PRIMARY KEY AUTO_INCREMENT,
        `key` VARCHAR(100) UNIQUE NOT NULL,
        value TEXT
    )''')
    
    # Check if admin exists
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if c.fetchone() is None:
        # Insert default user (admin)
        admin_pw = generate_password_hash('admin123')
        c.execute('''INSERT INTO users (username, password, email, full_name, role)
                     VALUES (%s, %s, %s, %s, %s)''',
                  ('admin', admin_pw, 'admin@ponpay.com', 'Admin PonPay', 'admin'))
        
        # Insert default wallet
        c.execute('INSERT INTO wallet (user_id, balance) VALUES (%s, %s)', (1, 25657000))

        # Insert dummy data santri (20 santri)
        santri_data = [
            ('Ahmad Ridho Kusuma', '2024001', 'Kelas 1', 'Laki-laki', '089123456789', 'Budi Kusuma', '085123456789', 'Jl. Merdeka No. 10'),
            ('Siti Nurhaliza', '2024002', 'Kelas 1', 'Perempuan', '089123456790', 'Nurul Hidayah', '085123456790', 'Jl. Ahmad Yani No. 5'),
            ('Muhammad Hasan', '2024003', 'Kelas 2', 'Laki-laki', '089123456791', 'Hasan Ali', '085123456791', 'Jl. Jendral Sudirman No. 8'),
            ('Fatima Azzahra', '2024004', 'Kelas 2', 'Perempuan', '089123456792', 'Zahra Hasanah', '085123456792', 'Jl. Gatot Subroto No. 12'),
            ('Rani Gunawan', '2024005', 'Kelas 1', 'Perempuan', '089123456793', 'Gunawan Santoso', '085123456793', 'Jl. Diponegoro No. 3'),
            ('Ismail Rahman', '2024006', 'Kelas 3', 'Laki-laki', '089123456794', 'Rahman Mahfud', '085123456794', 'Jl. Imam Bonjol No. 15'),
            ('Nurul Iman', '2024007', 'Kelas 2', 'Perempuan', '089123456795', 'Iman Santoso', '085123456795', 'Jl. Kartini No. 7'),
            ('Bilal Ibrahim', '2024008', 'Kelas 1', 'Laki-laki', '089123456796', 'Ibrahim Salim', '085123456796', 'Jl. Ahmad Dahlan No. 20'),
            ('Laila Muqdas', '2024009', 'Kelas 3', 'Perempuan', '089123456797', 'Muqdas Hidayat', '085123456797', 'Jl. Hasanuddin No. 11'),
            ('Amir Fatah', '2024010', 'Kelas 2', 'Laki-laki', '089123456798', 'Fatah Rahman', '085123456798', 'Jl. Maulana No. 6'),
            ('Salma Hayati', '2024011', 'Kelas 1', 'Perempuan', '089123456799', 'Hayati Wijaya', '085123456799', 'Jl. Kebumen No. 9'),
            ('Hamid Syaraf', '2024012', 'Kelas 3', 'Laki-laki', '089123456800', 'Syaraf Ahmad', '085123456800', 'Jl. Raya No. 2'),
            ('Zainab Farah', '2024013', 'Kelas 2', 'Perempuan', '089123456801', 'Farah Mahmud', '085123456801', 'Jl. Cendrawasih No. 14'),
            ('Rafiq Hamdani', '2024014', 'Kelas 1', 'Laki-laki', '089123456802', 'Hamdani Karman', '085123456802', 'Jl. Pendidikan No. 4'),
            ('Yasmin Nurdin', '2024015', 'Kelas 3', 'Perempuan', '089123456803', 'Nurdin Anwar', '085123456803', 'Jl. Batu No. 16'),
            ('Karim Mahmud', '2024016', 'Kelas 2', 'Laki-laki', '089123456804', 'Mahmud Azis', '085123456804', 'Jl. Sungai No. 8'),
            ('Dina Putri', '2024017', 'Kelas 1', 'Perempuan', '089123456805', 'Putri Santoso', '085123456805', 'Jl. Bukit No. 13'),
            ('Faiz Abrar', '2024018', 'Kelas 3', 'Laki-laki', '089123456806', 'Abrar Salman', '085123456806', 'Jl. Gunung No. 1'),
            ('Halim Fadli', '2024019', 'Kelas 2', 'Laki-laki', '089123456807', 'Fadli Rohman', '085123456807', 'Jl. Terang No. 19'),
            ('Nadia Kusuma', '2024020', 'Kelas 1', 'Perempuan', '089123456808', 'Kusuma Wijaya', '085123456808', 'Jl. Jaya No. 18'),
        ]
        
        for data in santri_data:
            c.execute('''INSERT INTO students (name, nisn, kelas, jenis_kelamin, phone, parent_name, parent_phone, alamat, status)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', data + ('aktif',))
        
        # Insert default settings
        c.execute('INSERT INTO settings (`key`, value) VALUES (%s, %s)', 
                  ('pondok_name', 'Pondok Pesantren Al Huda'))
        c.execute('INSERT INTO settings (`key`, value) VALUES (%s, %s)', 
                  ('system_currency', 'IDR'))
    
    db.commit()
    c.close()

def query_db(query, args=(), one=False):
    """Query database dengan parameter"""
    cursor = get_db().cursor(dictionary=True)
    cursor.execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    """Execute query (INSERT, UPDATE, DELETE)"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, args)
    db.commit()
    last_id = cursor.lastrowid
    cursor.close()
    return last_id


### User helpers ###
def get_all_users():
    return query_db('SELECT id, username, email, full_name, role, profile_picture, created_at FROM users ORDER BY id')

def get_user(user_id):
    return query_db('SELECT * FROM users WHERE id = %s', (user_id,), one=True)

def get_user_by_username(username):
    return query_db('SELECT * FROM users WHERE username = %s', (username,), one=True)

def create_user(username, password, email='', full_name='', role='user'):
    pw_hash = generate_password_hash(password)
    return execute_db('INSERT INTO users (username, password, email, full_name, role) VALUES (%s, %s, %s, %s, %s)',
                      (username, pw_hash, email, full_name, role))

def update_user(user_id, username, email, full_name, role):
    return execute_db('UPDATE users SET username = %s, email = %s, full_name = %s, role = %s WHERE id = %s',
                      (username, email, full_name, role, user_id))

def set_user_password(user_id, new_password):
    pw_hash = generate_password_hash(new_password)
    return execute_db('UPDATE users SET password = %s WHERE id = %s', (pw_hash, user_id))

def delete_user(user_id):
    return execute_db('DELETE FROM users WHERE id = %s', (user_id,))

def get_dashboard_stats(user_id=1):
    """Mendapatkan statistik dashboard"""
    today = datetime.now()
    start_of_month = datetime(today.year, today.month, 1)
    
    # Total pemasukan bulan ini
    income = query_db('''
        SELECT COALESCE(SUM(amount), 0) as total 
        FROM transactions 
        WHERE user_id = %s AND type = 'income' AND date >= %s
    ''', (user_id, start_of_month.strftime('%Y-%m-%d')), one=True)
    
    # Total pengeluaran bulan ini
    expense = query_db('''
        SELECT COALESCE(SUM(amount), 0) as total 
        FROM transactions 
        WHERE user_id = %s AND type = 'expense' AND date >= %s
    ''', (user_id, start_of_month.strftime('%Y-%m-%d')), one=True)
    
    # Jumlah transaksi bulan ini
    count = query_db('''
        SELECT COUNT(*) as total 
        FROM transactions 
        WHERE user_id = %s AND date >= %s
    ''', (user_id, start_of_month.strftime('%Y-%m-%d')), one=True)
    
    # Saldo saat ini
    wallet = query_db('SELECT balance FROM wallet WHERE user_id = %s', (user_id,), one=True)
    
    # Transaksi terakhir (5 transaksi)
    recent = query_db('''
        SELECT * FROM transactions 
        WHERE user_id = %s 
        ORDER BY date DESC, created_at DESC 
        LIMIT 5
    ''', (user_id,))
    
    return {
        'total_income': income['total'] if income else 0,
        'total_expense': expense['total'] if expense else 0,
        'total_transactions': count['total'] if count else 0,
        'balance': wallet['balance'] if wallet else 0,
        'recent_transactions': recent
    }

def get_monthly_stats(user_id=1, months=1):
    """Mendapatkan statistik per bulan"""
    today = datetime.now()
    start_date = today - timedelta(days=30*months)
    
    data = query_db('''
        SELECT 
            DATE_FORMAT(date, '%%Y-%%m') as month,
            type,
            SUM(amount) as total
        FROM transactions
        WHERE user_id = %s AND date >= %s
        GROUP BY month, type
        ORDER BY month
    ''', (user_id, start_date.strftime('%Y-%m-%d')))
    
    return data

def get_category_stats(user_id=1, trans_type='expense', months=1):
    """Mendapatkan statistik per kategori"""
    today = datetime.now()
    start_date = today - timedelta(days=30*months)
    
    data = query_db('''
        SELECT 
            category,
            SUM(amount) as total
        FROM transactions
        WHERE user_id = %s AND type = %s AND date >= %s
        GROUP BY category
        ORDER BY total DESC
    ''', (user_id, trans_type, start_date.strftime('%Y-%m-%d')))
    
    return data


# ===== FUNCTIONS UNTUK STUDENTS =====

def get_all_students():
    """Mendapatkan semua santri"""
    return query_db('''
        SELECT * FROM students 
        ORDER BY kelas, name ASC
    ''')

def get_student(student_id):
    """Mendapatkan detail santri"""
    return query_db('SELECT * FROM students WHERE id = %s', (student_id,), one=True)

def get_student_payments(student_id):
    """Mendapatkan riwayat pembayaran santri"""
    return query_db('''
        SELECT * FROM transactions 
        WHERE student_id = %s AND type = 'income'
        ORDER BY date DESC, created_at DESC
    ''', (student_id,))

def get_student_payment_stats(student_id):
    """Mendapatkan statistik pembayaran santri"""
    today = datetime.now()
    start_of_month = datetime(today.year, today.month, 1)
    
    # Total pembayaran bulan ini
    month_payment = query_db('''
        SELECT COALESCE(SUM(amount), 0) as total 
        FROM transactions 
        WHERE student_id = %s AND type = 'income' AND date >= %s
    ''', (student_id, start_of_month.strftime('%Y-%m-%d')), one=True)
    
    # Total pembayaran semua waktu
    total_payment = query_db('''
        SELECT COALESCE(SUM(amount), 0) as total 
        FROM transactions 
        WHERE student_id = %s AND type = 'income'
    ''', (student_id,), one=True)
    
    # Jumlah pembayaran
    payment_count = query_db('''
        SELECT COUNT(*) as total 
        FROM transactions 
        WHERE student_id = %s AND type = 'income'
    ''', (student_id,), one=True)
    
    # Pembayaran terakhir
    last_payment = query_db('''
        SELECT * FROM transactions 
        WHERE student_id = %s AND type = 'income'
        ORDER BY date DESC LIMIT 1
    ''', (student_id,), one=True)
    
    return {
        'month_payment': month_payment['total'] if month_payment else 0,
        'total_payment': total_payment['total'] if total_payment else 0,
        'payment_count': payment_count['total'] if payment_count else 0,
        'last_payment': last_payment
    }

def add_student(name, nisn, kelas, jenis_kelamin, phone, parent_name, parent_phone, alamat, status='aktif'):
    """Menambah santri baru"""
    return execute_db('''
        INSERT INTO students (name, nisn, kelas, jenis_kelamin, phone, parent_name, parent_phone, alamat, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (name, nisn, kelas, jenis_kelamin, phone, parent_name, parent_phone, alamat, status))

def update_student(student_id, name, nisn, kelas, jenis_kelamin, phone, parent_name, parent_phone, alamat, status):
    """Update data santri"""
    return execute_db('''
        UPDATE students 
        SET name=%s, nisn=%s, kelas=%s, jenis_kelamin=%s, phone=%s, parent_name=%s, parent_phone=%s, alamat=%s, status=%s
        WHERE id=%s
    ''', (name, nisn, kelas, jenis_kelamin, phone, parent_name, parent_phone, alamat, status, student_id))


def update_student_photo(student_id, photo_path):
    """Update path to student photo"""
    return execute_db('UPDATE students SET photo = %s WHERE id = %s', (photo_path, student_id))

def update_user_profile_picture(user_id, picture_path):
    """Update user's profile_picture path"""
    return execute_db('UPDATE users SET profile_picture = %s WHERE id = %s', (picture_path, user_id))

def delete_student(student_id):
    """Menghapus santri"""
    return execute_db('DELETE FROM students WHERE id=%s', (student_id,))


def ensure_history_table():
    """Ensure history table exists (safe to call multiple times)."""
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT,
            action VARCHAR(50) NOT NULL,
            target_type VARCHAR(50),
            target_id INT,
            meta TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()
    cur.close()


def record_history(user_id, action, target_type=None, target_id=None, meta=None):
    """Record an action into history log."""
    return execute_db('''
        INSERT INTO history (user_id, action, target_type, target_id, meta)
        VALUES (%s, %s, %s, %s, %s)
    ''', (user_id, action, target_type, target_id, meta))


def get_history(limit=200):
    """Get recent history entries ordered by newest first."""
    return query_db('SELECT * FROM history ORDER BY created_at DESC LIMIT %s', (limit,))


### Bills / Tagihan helpers ###
def ensure_bills_table():
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INT PRIMARY KEY AUTO_INCREMENT,
            student_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            amount INT NOT NULL,
            due_date VARCHAR(20),
            status VARCHAR(20) DEFAULT 'unpaid',
            created_by INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            paid_at TIMESTAMP NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')
    db.commit()
    cur.close()


def create_bill(student_id, title, amount, due_date=None, created_by=None):
    return execute_db('''
        INSERT INTO bills (student_id, title, amount, due_date, created_by) VALUES (%s, %s, %s, %s, %s)
    ''', (student_id, title, amount, due_date, created_by))


def get_all_bills():
    return query_db('SELECT b.*, s.name as student_name, s.nisn as student_nisn FROM bills b LEFT JOIN students s ON b.student_id = s.id ORDER BY b.created_at DESC')


def get_bill(bill_id):
    return query_db('SELECT * FROM bills WHERE id = %s', (bill_id,), one=True)


def update_bill(bill_id, student_id, title, amount, due_date, status):
    return execute_db('''
        UPDATE bills SET student_id = %s, title = %s, amount = %s, due_date = %s, status = %s WHERE id = %s
    ''', (student_id, title, amount, due_date, status, bill_id))


def delete_bill(bill_id):
    return execute_db('DELETE FROM bills WHERE id = %s', (bill_id,))


def mark_bill_paid(bill_id, paid_at=None):
    paid_at = paid_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # set status and paid_at
    return execute_db('UPDATE bills SET status = %s, paid_at = %s WHERE id = %s', ('paid', paid_at, bill_id))


def get_student_bills(student_id):
    return query_db('SELECT * FROM bills WHERE student_id = %s ORDER BY created_at DESC', (student_id,))


def get_unpaid_bills_count():
    row = query_db('SELECT COUNT(*) as total FROM bills WHERE status = "unpaid"', (), one=True)
    return row['total'] if row else 0


def get_student_unpaid_amount(student_id):
    """Hitung total kekurangan pembayaran per santri"""
    row = query_db('SELECT COALESCE(SUM(amount), 0) as total FROM bills WHERE student_id = %s AND status = "unpaid"', (student_id,), one=True)
    return row['total'] if row else 0


def get_bill_stats_by_class():
    """Mengambil total tunggakan per kelas"""
    return query_db('''
        SELECT s.kelas, SUM(b.amount) as total_unpaid
        FROM bills b
        JOIN students s ON b.student_id = s.id
        WHERE b.status = 'unpaid'
        GROUP BY s.kelas
        ORDER BY total_unpaid DESC
    ''')
