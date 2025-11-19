"""
PonPay - Sistem Pembayaran Pondok Pesantren Al Huda
Main Flask Application
"""
from flask import Flask, render_template
from db import init_db, get_db, close_db, ensure_history_table
import locale
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ponpay-secret-key-2025'
app.config['DATABASE'] = 'ponpay.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max file size

# Inisialisasi database
def init_app():
    """Inisialisasi aplikasi Flask"""
    with app.app_context():
        init_db()
        # ensure history table exists even if DB already present
        try:
            ensure_history_table()
        except Exception:
            pass
        try:
            from db import ensure_bills_table
            ensure_bills_table()
        except Exception:
            pass
        
    app.teardown_appcontext(close_db)

# Custom Jinja2 filter untuk format Rupiah
@app.template_filter('rupiah')
def rupiah_format(value):
    """Format nilai uang ke Rupiah"""
    try:
        value = int(value) if isinstance(value, (int, float)) else int(value)
        return f"Rp {value:,.0f}".replace(',', '.')
    except (ValueError, TypeError):
        return "Rp 0"

@app.template_filter('format_date')
def format_date(date_string):
    """Format tanggal Indonesia"""
    months = {
        'January': 'Januari', 'February': 'Februari', 'March': 'Maret',
        'April': 'April', 'May': 'Mei', 'June': 'Juni',
        'July': 'Juli', 'August': 'Agustus', 'September': 'September',
        'October': 'Oktober', 'November': 'November', 'December': 'Desember'
    }
    try:
        if isinstance(date_string, str):
            dt = datetime.strptime(date_string, '%Y-%m-%d')
        else:
            dt = date_string
        
        day = dt.day
        month_en = dt.strftime('%B')
        year = dt.year
        month_id = months.get(month_en, month_en)
        
        return f"{day} {month_id} {year}"
    except:
        return str(date_string)

# Import routes setelah membuat app
from routes import auth_bp, dashboard_bp, transaction_bp, statistics_bp, wallet_bp, settings_bp, students_bp, history_bp, create_home_routes, users_bp, payments_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(transaction_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(wallet_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(students_bp)
app.register_blueprint(history_bp)
app.register_blueprint(users_bp)
app.register_blueprint(payments_bp)

# Create home routes
create_home_routes(app)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_app()
    app.run(debug=True)
