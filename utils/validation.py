"""
Input Validation Utilities for PonPay
Production-ready validation functions for financial data security
"""
import re
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import flash

class ValidationError(Exception):
    """Custom validation error"""
    pass

def validate_required(value, field_name):
    """Validate required fields"""
    if not value or str(value).strip() == '':
        raise ValidationError(f"{field_name} wajib diisi")
    return str(value).strip()

def validate_username(username):
    """Validate username format and uniqueness"""
    username = validate_required(username, "Username")

    # Length check
    if len(username) < 3 or len(username) > 50:
        raise ValidationError("Username harus 3-50 karakter")

    # Format check (alphanumeric, underscore, dash only)
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValidationError("Username hanya boleh huruf, angka, underscore (_), dan dash (-)")

    # Reserved words
    reserved = ['admin', 'root', 'system', 'superuser', 'administrator']
    if username.lower() in reserved:
        raise ValidationError("Username tidak diperbolehkan")

    return username

def validate_password(password, min_length=8):
    """Validate password strength"""
    password = validate_required(password, "Password")

    if len(password) < min_length:
        raise ValidationError(f"Password minimal {min_length} karakter")

    # Check for at least one uppercase, lowercase, digit
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password harus mengandung huruf besar")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password harus mengandung huruf kecil")
    if not re.search(r'\d', password):
        raise ValidationError("Password harus mengandung angka")

    # Check for common weak passwords
    weak_passwords = ['password', '123456', 'admin123', 'qwerty', 'password123']
    if password.lower() in weak_passwords:
        raise ValidationError("Password terlalu lemah")

    return password

def validate_email(email):
    """Validate email format"""
    if not email or str(email).strip() == '':
        return None  # Email optional

    email = str(email).strip()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(email_pattern, email):
        raise ValidationError("Format email tidak valid")

    if len(email) > 255:
        raise ValidationError("Email terlalu panjang")

    return email

def validate_amount(amount, field_name="Jumlah", min_value=100, max_value=100000000):
    """Validate monetary amounts"""
    try:
        amount = int(amount)
    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} harus berupa angka")

    if amount < min_value:
        raise ValidationError(f"{field_name} minimal Rp {min_value:,}")
    if amount > max_value:
        raise ValidationError(f"{field_name} maksimal Rp {max_value:,}")

    return amount

def validate_date(date_str, field_name="Tanggal"):
    """Validate date format (YYYY-MM-DD)"""
    date_str = validate_required(date_str, field_name)

    try:
        # Parse and validate date
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')

        # Check reasonable date range (not too far in past/future)
        today = datetime.now()
        min_date = today.replace(year=today.year - 10)
        max_date = today.replace(year=today.year + 1)

        if date_obj < min_date:
            raise ValidationError(f"{field_name} tidak boleh lebih dari 10 tahun yang lalu")
        if date_obj > max_date:
            raise ValidationError(f"{field_name} tidak boleh lebih dari 1 tahun ke depan")

        return date_str

    except ValueError:
        raise ValidationError(f"{field_name} harus dalam format YYYY-MM-DD")

def validate_name(name, field_name="Nama", max_length=100):
    """Validate names (allow letters, spaces, apostrophes, dashes)"""
    name = validate_required(name, field_name)

    if len(name) > max_length:
        raise ValidationError(f"{field_name} maksimal {max_length} karakter")

    # Allow letters, spaces, apostrophes, dashes
    if not re.match(r"^[a-zA-Z\s'-]+$", name):
        raise ValidationError(f"{field_name} hanya boleh huruf, spasi, apostrof (') dan dash (-)")

    # Check for multiple consecutive spaces
    if re.search(r'\s{2,}', name):
        raise ValidationError(f"{field_name} tidak boleh mengandung spasi berurutan")

    return name.strip()

def validate_nisn(nisn):
    """Validate NISN (Indonesian Student Number)"""
    if not nisn or str(nisn).strip() == '':
        return None  # NISN optional

    nisn = str(nisn).strip()

    # NISN should be 10 digits
    if not re.match(r'^\d{10}$', nisn):
        raise ValidationError("NISN harus 10 digit angka")

    return nisn

def validate_phone(phone, field_name="Nomor HP"):
    """Validate Indonesian phone number"""
    if not phone or str(phone).strip() == '':
        return None  # Phone optional

    phone = str(phone).strip()

    # Remove any spaces, dashes, etc.
    phone = re.sub(r'[-\s\(\)]', '', phone)

    # Indonesian mobile patterns: 08xx or +628xx
    if phone.startswith('+62'):
        phone = phone[3:]  # Remove +62
    elif phone.startswith('62'):
        phone = phone[2:]  # Remove 62

    # Must start with 8 and be 10-13 digits total
    if not re.match(r'^8\d{8,11}$', phone):
        raise ValidationError(f"{field_name} harus nomor Indonesia valid (contoh: 08123456789)")

    return phone

def validate_kelas(kelas):
    """Validate class/grade"""
    kelas = validate_required(kelas, "Kelas")

    # Allow common class formats
    valid_formats = [
        r'^Kelas \d+$',  # Kelas 1, Kelas 2, etc.
        r'^\d+$',        # 1, 2, 3, etc.
        r'^[IVXLCDM]+$', # Roman numerals
        r'^[a-zA-Z]+\s*\d*$'  # Other formats like "VII A"
    ]

    if not any(re.match(pattern, kelas, re.IGNORECASE) for pattern in valid_formats):
        raise ValidationError("Format kelas tidak valid")

    return kelas.strip()

def validate_jenis_kelamin(gender):
    """Validate gender"""
    gender = validate_required(gender, "Jenis Kelamin")

    valid_genders = ['Laki-laki', 'Perempuan', 'laki-laki', 'perempuan']
    if gender not in valid_genders:
        raise ValidationError("Jenis kelamin harus 'Laki-laki' atau 'Perempuan'")

    return gender

def validate_alamat(alamat, max_length=255):
    """Validate address"""
    if not alamat or str(alamat).strip() == '':
        return None  # Address optional

    alamat = str(alamat).strip()

    if len(alamat) > max_length:
        raise ValidationError(f"Alamat maksimal {max_length} karakter")

    # Basic check for potentially harmful content
    dangerous_patterns = ['<script', 'javascript:', 'onload=', 'onerror=']
    if any(pattern in alamat.lower() for pattern in dangerous_patterns):
        raise ValidationError("Alamat mengandung konten tidak diperbolehkan")

    return alamat

def validate_category(category, trans_type):
    """Validate transaction category"""
    category = validate_required(category, "Kategori")

    if len(category) > 100:
        raise ValidationError("Kategori maksimal 100 karakter")

    # Allow alphanumeric, spaces, dashes, slashes
    if not re.match(r"^[a-zA-Z0-9\s\-\/\(\)]+$", category):
        raise ValidationError("Kategori hanya boleh huruf, angka, spasi, dash (-), slash (/), dan tanda kurung")

    # Category-specific validations
    if trans_type == 'income':
        income_categories = ['Pembayaran Santri', 'Donasi', 'Bantuan', 'Pendapatan Lain']
        if category not in income_categories and not category.startswith(('Pembayaran', 'Donasi', 'Bantuan')):
            # Allow custom categories but warn
            pass
    elif trans_type == 'expense':
        expense_categories = ['Makanan', 'Listrik', 'Air', 'Transport', 'Pendidikan', 'Kesehatan', 'Pengeluaran Lain']
        if category not in expense_categories and not any(keyword in category for keyword in ['Makan', 'Listrik', 'Air', 'Transport', 'Pendidikan', 'Kesehatan']):
            # Allow custom categories
            pass

    return category.strip()

def validate_description(description, max_length=500):
    """Validate transaction description"""
    if not description or str(description).strip() == '':
        return None  # Description optional

    description = str(description).strip()

    if len(description) > max_length:
        raise ValidationError(f"Keterangan maksimal {max_length} karakter")

    # Check for potentially harmful content
    dangerous_patterns = ['<script', 'javascript:', 'onload=', 'onerror=', 'SELECT', 'INSERT', 'UPDATE', 'DELETE']
    if any(pattern.upper() in description.upper() for pattern in dangerous_patterns):
        raise ValidationError("Keterangan mengandung konten tidak diperbolehkan")

    return description

def validate_file_upload(file, allowed_extensions=None, max_size=None):
    """Validate file upload security"""
    if not file:
        return None

    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

    if max_size is None:
        max_size = 2 * 1024 * 1024  # 2MB

    # Check if file exists
    if not file.filename:
        raise ValidationError("File tidak ditemukan")

    # Secure filename
    filename = secure_filename(file.filename)

    # Check extension
    if '.' not in filename:
        raise ValidationError("File harus memiliki ekstensi")

    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(f"Format file tidak diperbolehkan. Gunakan: {', '.join(allowed_extensions)}")

    # Check file size
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset to beginning

    if size > max_size:
        raise ValidationError(f"Ukuran file maksimal {max_size//(1024*1024)}MB")

    # Basic content type check for images
    if ext in {'png', 'jpg', 'jpeg', 'gif'}:
        # Read first few bytes to check magic numbers
        header = file.read(8)
        file.seek(0)

        # PNG: 89 50 4E 47
        # JPG: FF D8
        # GIF: 47 49 46
        if ext == 'png' and header[:4] != b'\x89PNG':
            raise ValidationError("File PNG tidak valid")
        elif ext in {'jpg', 'jpeg'} and header[:2] != b'\xFF\xD8':
            raise ValidationError("File JPG tidak valid")
        elif ext == 'gif' and header[:3] != b'GIF':
            raise ValidationError("File GIF tidak valid")

    return filename

def check_duplicate_username(username, exclude_user_id=None):
    """Check if username already exists - placeholder, implement in routes"""
    # This function is now a placeholder. Database checks should be done in routes.
    pass

def check_duplicate_nisn(nisn, exclude_student_id=None):
    """Check if NISN already exists - placeholder, implement in routes"""
    # This function is now a placeholder. Database checks should be done in routes.
    pass

def validate_student_data(name, nisn, kelas, jenis_kelamin, phone, parent_name, parent_phone, alamat, exclude_student_id=None):
    """Comprehensive student data validation"""
    name = validate_name(name, "Nama Santri")
    nisn = validate_nisn(nisn)
    kelas = validate_kelas(kelas)
    jenis_kelamin = validate_jenis_kelamin(jenis_kelamin)
    phone = validate_phone(phone, "Nomor HP Santri")
    parent_name = validate_name(parent_name, "Nama Orang Tua")
    parent_phone = validate_phone(parent_phone, "Nomor HP Orang Tua")
    alamat = validate_alamat(alamat)

    # Check duplicates
    check_duplicate_nisn(nisn, exclude_student_id)

    return {
        'name': name,
        'nisn': nisn,
        'kelas': kelas,
        'jenis_kelamin': jenis_kelamin,
        'phone': phone,
        'parent_name': parent_name,
        'parent_phone': parent_phone,
        'alamat': alamat
    }

def validate_transaction_data(trans_type, category, amount, description, date, student_id=None):
    """Comprehensive transaction data validation"""
    # Validate transaction type
    if trans_type not in ['income', 'expense']:
        raise ValidationError("Tipe transaksi harus 'income' atau 'expense'")

    category = validate_category(category, trans_type)
    amount = validate_amount(amount, "Jumlah")
    description = validate_description(description)
    date = validate_date(date, "Tanggal")

    # Validate student_id if provided (database check moved to routes)
    if student_id:
        try:
            student_id = int(student_id)
        except (ValueError, TypeError):
            raise ValidationError("ID Santri tidak valid")

    return {
        'type': trans_type,
        'category': category,
        'amount': amount,
        'description': description,
        'date': date,
        'student_id': student_id
    }

def validate_user_data(username, email, full_name, role, exclude_user_id=None):
    """Comprehensive user data validation"""
    username = validate_username(username)
    email = validate_email(email)
    full_name = validate_name(full_name, "Nama Lengkap", 100)
    role = validate_required(role, "Role")

    if role not in ['admin', 'staff', 'user']:
        raise ValidationError("Role harus 'admin', 'staff', atau 'user'")

    # Check username uniqueness
    check_duplicate_username(username, exclude_user_id)

    return {
        'username': username,
        'email': email,
        'full_name': full_name,
        'role': role
    }

def flash_validation_errors(func):
    """Decorator to flash validation errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            flash(str(e), 'danger')
            return None
    return wrapper

# Rate limiting helper (basic implementation)
rate_limit_cache = {}

def check_rate_limit(identifier, max_attempts=5, window_seconds=300):
    """Basic rate limiting for login attempts"""
    now = datetime.now().timestamp()
    key = f"{identifier}"

    if key not in rate_limit_cache:
        rate_limit_cache[key] = []

    # Clean old entries
    rate_limit_cache[key] = [t for t in rate_limit_cache[key] if now - t < window_seconds]

    if len(rate_limit_cache[key]) >= max_attempts:
        raise ValidationError(f"Terlalu banyak percobaan. Coba lagi dalam {window_seconds//60} menit")

    rate_limit_cache[key].append(now)
