/**
 * PonPay - Main JavaScript
 * Sistem Pembayaran Pondok Pesantren Al Huda
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
    initializeSidebarCollapse();
    initializeTooltips();
    initializeAnimations();
});

/**
 * Initialize Sidebar
 */
function initializeSidebar() {
    const toggleBtn = document.querySelector('.btn-sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const sidebarNav = document.querySelector('.sidebar-nav');

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (sidebar) {
                sidebar.classList.toggle('active');
                document.body.classList.toggle('sidebar-open');
            }
        });
    }

    // Close sidebar when clicking outside (mobile only)
    document.addEventListener('click', function(event) {
        if (sidebar && sidebar.classList.contains('active')) {
            if (!sidebar.contains(event.target) && !toggleBtn?.contains(event.target)) {
                sidebar.classList.remove('active');
                document.body.classList.remove('sidebar-open');
            }
        }
    });

    // Close sidebar ketika link di klik pada mobile
    if (sidebarNav) {
        const navLinks = sidebarNav.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                // Jangan close jika collapse toggle
                if (!this.getAttribute('data-bs-toggle')) {
                    if (window.innerWidth <= 768 && !this.getAttribute('data-bs-toggle')) {
                        setTimeout(() => {
                            sidebar.classList.remove('active');
                            document.body.classList.remove('sidebar-open');
                        }, 100);
                    }
                }
            });
        });
    }

    // Handle window resize to ensure sidebar state is correct
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            // On desktop, ensure sidebar is always visible
            if (sidebar) {
                sidebar.classList.remove('active');
                document.body.classList.remove('sidebar-open');
            }
        }
    });
}

/**
 * Initialize Tooltips
 */
function initializeTooltips() {
    // Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize Animations
 */
function initializeAnimations() {
    // Animate stat cards
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.animation = `fadeInUp 0.5s ease ${index * 0.1}s both`;
    });

    // Animate balance card
    const balanceCard = document.querySelector('.balance-card');
    if (balanceCard) {
        balanceCard.style.animation = 'fadeInDown 0.5s ease';
    }
}

/**
 * Format Currency to Rupiah
 */
function formatRupiah(number) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(number);
}

/**
 * Format Date
 */
function formatDate(dateString) {
    const months = [
        'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
    ];

    const date = new Date(dateString);
    const day = date.getDate();
    const month = months[date.getMonth()];
    const year = date.getFullYear();

    return `${day} ${month} ${year}`;
}

/**
 * Show Toast Notification
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        <div class="d-flex align-items-center gap-2">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.5s ease';
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

/**
 * Confirm Delete
 */
function confirmDelete(message = 'Apakah Anda yakin ingin menghapus?') {
    return confirm(message);
}

/**
 * Filter Form Submission
 */
function submitFilterForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.submit();
    }
}

/**
 * Print Document
 */
function printPage() {
    window.print();
}

/**
 * Export to CSV
 */
function exportToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        let csvRow = [];
        cols.forEach(col => {
            csvRow.push('"' + col.innerText.replace(/"/g, '""') + '"');
        });
        csv.push(csvRow.join(','));
    });

    downloadCSV(csv.join('\n'), filename);
}

/**
 * Download CSV
 */
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], { type: 'text/csv' });
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(csvFile);
    downloadLink.download = filename;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

/**
 * Format Large Numbers
 */
function formatNumber(number) {
    if (number >= 1000000) {
        return (number / 1000000).toFixed(2) + 'M';
    } else if (number >= 1000) {
        return (number / 1000).toFixed(2) + 'K';
    }
    return number.toString();
}

/**
 * Calculate Summary Stats
 */
function calculateStats(transactions) {
    let income = 0;
    let expense = 0;
    let totalTransactions = transactions.length;

    transactions.forEach(trans => {
        if (trans.type === 'income') {
            income += trans.amount;
        } else {
            expense += trans.amount;
        }
    });

    return {
        income,
        expense,
        balance: income - expense,
        totalTransactions
    };
}

/**
 * Add event listeners to buttons
 */
function initializeEventListeners() {
    // Delete buttons
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirmDelete()) {
                e.preventDefault();
            }
        });
    });

    // Print button
    const printBtn = document.querySelector('.btn-print');
    if (printBtn) {
        printBtn.addEventListener('click', printPage);
    }

    // Export button
    const exportBtn = document.querySelector('.btn-export');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            exportToCSV('transactionsTable', 'transaksi_' + new Date().getTime() + '.csv');
        });
    }
}

// Call event listeners initialization
initializeEventListeners();

/**
 * Dark Mode Toggle (Optional)
 */
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

/**
 * Load Dark Mode preference
 */
function loadDarkModePreference() {
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }
}

// Load dark mode preference on page load
window.addEventListener('load', loadDarkModePreference);

/**
 * Animations CSS
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeOut {
        from {
            opacity: 1;
        }
        to {
            opacity: 0;
        }
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }

    /* Dark Mode */
    body.dark-mode {
        background-color: #1a1a1a;
        color: #e0e0e0;
    }

    body.dark-mode .card {
        background-color: #2d2d2d;
        color: #e0e0e0;
    }

    body.dark-mode .form-control,
    body.dark-mode .form-select {
        background-color: #3d3d3d;
        color: #e0e0e0;
        border-color: #4d4d4d;
    }

    body.dark-mode .table {
        color: #e0e0e0;
    }

    body.dark-mode .table-light {
        background-color: #3d3d3d;
    }

    body.dark-mode .top-navbar {
        background-color: #2d2d2d;
        border-color: #4d4d4d;
    }
`;
document.head.appendChild(style);

/**
 * Real-time Clock
 */
function updateClock() {
    const clock = document.querySelector('.clock');
    if (clock) {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        clock.textContent = `${hours}:${minutes}:${seconds}`;
    }
}

setInterval(updateClock, 1000);
updateClock();

/**
 * Fetch & Render Data
 */
async function fetchData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        showToast('Gagal memuat data', 'danger');
        return null;
    }
}

/**
 * Post Data
 */
async function postData(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('Network response was not ok');
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        showToast('Gagal mengirim data', 'danger');
        return null;
    }
}

/**
 * Initialize Sidebar Collapse
 */
function initializeSidebarCollapse() {
    const collapseBtn = document.getElementById('sidebarCollapseBtn');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');

    if (collapseBtn && sidebar) {
        collapseBtn.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');

            // Adjust main content margin
            if (sidebar.classList.contains('collapsed')) {
                mainContent.style.marginLeft = '5.00rem';
            } else {
                mainContent.style.marginLeft = '20.00rem';
            }

            // Save state to localStorage
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        });
    }

    // Load saved state
    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (isCollapsed && sidebar) {
        sidebar.classList.add('collapsed');
        if (mainContent) {
            mainContent.style.marginLeft = '5.00rem';
        }
    }
}

/**
 * Smooth Scroll
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
