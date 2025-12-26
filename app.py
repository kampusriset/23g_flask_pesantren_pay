"""
PonPay - Sistem Pembayaran Pondok Pesantren Al Huda
Main Flask Application
"""
from flask import Flask, render_template, session, redirect, url_for, g, request
from flask_wtf.csrf import CSRFProtect
from db import init_db, get_db, close_db, ensure_history_table
import locale
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ponpay-secret-key-2025'

# CSRF Protection Configuration - Initialize EARLY before any routes
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'ponpay-csrf-secret-key-2025'
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour CSRF token validity
app.config['WTF_CSRF_METHODS'] = ['POST', 'PUT', 'PATCH', 'DELETE']

# Initialize CSRF Protection EARLY
csrf = CSRFProtect(app)

# Configure CSRF to only protect state-changing methods
app.config['WTF_CSRF_METHODS'] = ['POST', 'PUT', 'PATCH', 'DELETE']
# Database Configuration
app.config['DATABASE'] = 'ponpay.db'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max file size

# Configure logging
if not app.debug:
    # Production logging
    file_handler = RotatingFileHandler('logs/csrf_security.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

# CSRF Security Logger - Always active for security monitoring
csrf_logger = logging.getLogger('csrf_security')
csrf_logger.setLevel(logging.WARNING)
csrf_handler = RotatingFileHandler('logs/csrf_security.log', maxBytes=10240000, backupCount=10)
csrf_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s - IP: %(remote_addr)s - User-Agent: %(user_agent)s'
))
csrf_logger.addHandler(csrf_handler)

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

# CSRF Error Handler
@app.errorhandler(400)
def handle_csrf_error(e):
    """Handle CSRF token errors dengan pesan yang user-friendly dan logging"""
    from flask_wtf.csrf import CSRFError

    # Check if this is a CSRF error
    if isinstance(e, CSRFError) or 'csrf' in str(e.description).lower() or 'token' in str(e.description).lower():
        # Log CSRF attempt for security monitoring
        extra = {
            'remote_addr': request.remote_addr if hasattr(request, 'remote_addr') else 'Unknown',
            'user_agent': request.headers.get('User-Agent', 'Unknown') if hasattr(request, 'headers') else 'Unknown'
        }
        csrf_logger.warning(f"CSRF token validation failed - Endpoint: {request.endpoint if hasattr(request, 'endpoint') else 'Unknown'}, "
                           f"Method: {request.method if hasattr(request, 'method') else 'Unknown'}", extra=extra)

        return render_template('csrf_error.html', datetime=datetime), 400
    return render_template('400.html'), 400

if __name__ == '__main__':
    init_app()
    app.run(debug=True)
