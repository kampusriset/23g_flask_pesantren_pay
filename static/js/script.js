/**
 * PonPay - Main JavaScript
 * Sistem Pembayaran Pondok Pesantren Al Huda
 */

document.addEventListener("DOMContentLoaded", function () {
  initializeSidebar();
  initializeSidebarCollapse();
  initializeTooltips();
  initializeAnimations();
  initializeTicker();
  initializeNavbarScroll(); // Add scroll effect for navbar
});

/**
 * Initialize Sidebar
 */
function initializeSidebar() {
  const toggleBtn = document.querySelector(".btn-sidebar-toggle");
  const sidebar = document.querySelector(".sidebar");
  const sidebarNav = document.querySelector(".sidebar-nav");

  if (toggleBtn) {
    toggleBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      if (sidebar) {
        // If on mobile and sidebar is hidden via desktop pref, temporarily show it
        if (window.innerWidth <= 768 && sidebar.classList.contains("hidden")) {
          sidebar.classList.remove("hidden");
          sidebar.dataset.hiddenTemp = "true";
          sidebar.setAttribute("aria-hidden", "false");
        }

        sidebar.classList.toggle("active");
        document.body.classList.toggle("sidebar-open");
        // animate hamburger icon and update ARIA
        toggleBtn.classList.toggle("open");
        const expanded = String(toggleBtn.classList.contains("open"));
        toggleBtn.setAttribute("aria-expanded", expanded);
        // remove focus outline after click
        toggleBtn.blur();
      }
    });
  }

  // Close sidebar when clicking outside (mobile only)
  document.addEventListener("click", function (event) {
    if (sidebar && sidebar.classList.contains("active")) {
      if (
        !sidebar.contains(event.target) &&
        !toggleBtn?.contains(event.target)
      ) {
        sidebar.classList.remove("active");
        document.body.classList.remove("sidebar-open");
        // restore hidden state if it was temporarily removed for mobile
        if (sidebar.dataset.hiddenTemp === "true") {
          sidebar.classList.add("hidden");
          delete sidebar.dataset.hiddenTemp;
          sidebar.setAttribute("aria-hidden", "true");
        }
        // ensure hamburger returns to normal state
        if (toggleBtn) {
          toggleBtn.classList.remove("open");
          toggleBtn.setAttribute("aria-expanded", "false");
        }
      }
    }
  });

  // Close sidebar ketika link di klik pada mobile
  if (sidebarNav) {
    const navLinks = sidebarNav.querySelectorAll(".nav-link");
    navLinks.forEach((link) => {
      link.addEventListener("click", function () {
        // Jangan close jika collapse toggle
        if (!this.getAttribute("data-bs-toggle")) {
          if (
            window.innerWidth <= 768 &&
            !this.getAttribute("data-bs-toggle")
          ) {
            setTimeout(() => {
              sidebar.classList.remove("active");
              document.body.classList.remove("sidebar-open");
              // restore hidden state if it was temporarily removed for mobile
              if (sidebar.dataset.hiddenTemp === "true") {
                sidebar.classList.add("hidden");
                delete sidebar.dataset.hiddenTemp;
                sidebar.setAttribute("aria-hidden", "true");
              }
            }, 100);
          }
        }
      });
    });
  }

  // Handle window resize to ensure sidebar state is correct
  window.addEventListener("resize", function () {
    if (window.innerWidth > 768) {
      // On desktop, ensure sidebar is always visible
      if (sidebar) {
        sidebar.classList.remove("active");
        document.body.classList.remove("sidebar-open");
      }
    }
  });
}

/**
 * Initialize Tooltips
 */
function initializeTooltips() {
  // Bootstrap tooltips
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

/**
 * Initialize Animations
 */
function initializeAnimations() {
  // Animate stat cards
  const statCards = document.querySelectorAll(".stat-card");
  statCards.forEach((card, index) => {
    card.style.animation = `fadeInUp 0.5s ease ${index * 0.1}s both`;
  });

  // Animate balance card
  const balanceCard = document.querySelector(".balance-card");
  if (balanceCard) {
    balanceCard.style.animation = "fadeInDown 0.5s ease";
  }
}

/**
 * Initialize Top Ticker animation and responsiveness
 */
function initializeTicker() {
  const ticker = document.querySelector(".top-ticker");
  const track = ticker?.querySelector(".ticker-track");
  if (!ticker || !track) return;

  // Ensure the track has duplicated content for a smooth loop
  const children = Array.from(track.children);
  if (children.length && track.children.length < children.length * 2) {
    children.forEach((node) => track.appendChild(node.cloneNode(true)));
  }

  // Compute duration based on width so speed feels constant across screens
  const computeDuration = () => {
    const trackWidth = track.scrollWidth || track.getBoundingClientRect().width;
    const containerWidth = ticker.clientWidth || 1;
    const pxPerSecond = 80; // adjust speed here (px/s)
    const duration = Math.max(8, trackWidth / pxPerSecond);
    track.style.animationDuration = duration + "s";
  };

  // Initial compute and on resize
  computeDuration();
  let resizeTimer;
  window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(computeDuration, 150);
  });

  // Pause on hover/focus for accessibility
  ticker.addEventListener("mouseenter", () => {
    track.style.animationPlayState = "paused";
  });
  ticker.addEventListener("mouseleave", () => {
    track.style.animationPlayState = "running";
  });
  ticker.addEventListener("focusin", () => {
    track.style.animationPlayState = "paused";
  });
  ticker.addEventListener("focusout", () => {
    track.style.animationPlayState = "running";
  });
}

/**
 * Initialize Navbar Scroll Effect
 * Adds 'scrolled' class to navbar when user scrolls down
 */
function initializeNavbarScroll() {
  const navbar = document.querySelector(".top-navbar");

  if (!navbar) return;

  let lastScrollTop = 0;

  // Listen to scroll event on window
  window.addEventListener("scroll", function () {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    // Add scrolled class when scrolling down past 50px
    if (scrollTop > 50) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }

    lastScrollTop = scrollTop;
  }, { passive: true }); // passive for better scroll performance
}

/**
 * Format Currency to Rupiah
 */
function formatRupiah(number) {
  return new Intl.NumberFormat("id-ID", {
    style: "currency",
    currency: "IDR",
    minimumFractionDigits: 0,
  }).format(number);
}

/**
 * Format Date
 */
function formatDate(dateString) {
  const months = [
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember",
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
function showToast(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = `alert alert-${type} position-fixed`;
  toast.style.cssText =
    "top: 20px; right: 20px; z-index: 9999; min-width: 300px;";
  toast.innerHTML = `
        <div class="d-flex align-items-center gap-2">
            <i class="fas fa-${type === "success"
      ? "check-circle"
      : type === "danger"
        ? "exclamation-circle"
        : type === "warning"
          ? "exclamation-triangle"
          : "info-circle"
    }"></i>
            <span>${message}</span>
        </div>
    `;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = "fadeOut 0.5s ease";
    setTimeout(() => toast.remove(), 500);
  }, 3000);
}

/**
 * Confirm Delete
 */
function confirmDelete(message = "Apakah Anda yakin ingin menghapus?") {
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
function exportToCSV(tableId, filename = "export.csv") {
  const table = document.getElementById(tableId);
  if (!table) return;

  let csv = [];
  const rows = table.querySelectorAll("tr");

  rows.forEach((row) => {
    const cols = row.querySelectorAll("td, th");
    let csvRow = [];
    cols.forEach((col) => {
      csvRow.push('"' + col.innerText.replace(/"/g, '""') + '"');
    });
    csv.push(csvRow.join(","));
  });

  downloadCSV(csv.join("\n"), filename);
}

/**
 * Download CSV
 */
function downloadCSV(csv, filename) {
  const csvFile = new Blob([csv], { type: "text/csv" });
  const downloadLink = document.createElement("a");
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
    return (number / 1000000).toFixed(2) + "M";
  } else if (number >= 1000) {
    return (number / 1000).toFixed(2) + "K";
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

  transactions.forEach((trans) => {
    if (trans.type === "income") {
      income += trans.amount;
    } else {
      expense += trans.amount;
    }
  });

  return {
    income,
    expense,
    balance: income - expense,
    totalTransactions,
  };
}

/**
 * Add event listeners to buttons
 */
function initializeEventListeners() {
  // Delete buttons
  document.querySelectorAll(".btn-delete").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      if (!confirmDelete()) {
        e.preventDefault();
      }
    });
  });

  // Print button
  const printBtn = document.querySelector(".btn-print");
  if (printBtn) {
    printBtn.addEventListener("click", printPage);
  }

  // Export button
  const exportBtn = document.querySelector(".btn-export");
  if (exportBtn) {
    exportBtn.addEventListener("click", function () {
      exportToCSV(
        "transactionsTable",
        "transaksi_" + new Date().getTime() + ".csv"
      );
    });
  }

  // Dark mode toggle button
  const darkToggle = document.getElementById("darkModeToggle");
  if (darkToggle) {
    darkToggle.addEventListener("click", function () {
      toggleDarkMode();
    });
    // initialize UI state
    updateDarkModeToggleUI();
  }
}

// Call event listeners initialization
initializeEventListeners();

/**
 * Dark Mode Toggle (Optional)
 */
function toggleDarkMode() {
  document.body.classList.toggle("dark-mode");
  const enabled = document.body.classList.contains("dark-mode");
  localStorage.setItem("darkMode", enabled);
  updateDarkModeToggleUI();
}

/**
 * Load Dark Mode preference
 */
function loadDarkModePreference() {
  if (localStorage.getItem("darkMode") === "true") {
    document.body.classList.add("dark-mode");
  }
  // Update UI of toggle button if present
  updateDarkModeToggleUI();
}

// Load dark mode preference on page load
window.addEventListener("load", loadDarkModePreference);

/**
 * Update dark mode toggle button UI (icon + aria-pressed)
 */
function updateDarkModeToggleUI() {
  const btn = document.getElementById("darkModeToggle");
  if (!btn) return;
  const icon = btn.querySelector("i");
  const enabled = document.body.classList.contains("dark-mode");
  btn.setAttribute("aria-pressed", String(enabled));
  if (icon) {
    icon.classList.remove("fa-moon", "fa-sun");
    icon.classList.add(enabled ? "fa-sun" : "fa-moon");
  }
  // adjust button appearance
  if (enabled) {
    btn.classList.remove("btn-outline-secondary");
    btn.classList.add("btn-secondary");
  } else {
    btn.classList.remove("btn-secondary");
    btn.classList.add("btn-outline-secondary");
  }
}

/**
 * Animations CSS
 */
const style = document.createElement("style");
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
  const clock = document.querySelector(".clock");
  if (clock) {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const seconds = String(now.getSeconds()).padStart(2, "0");
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
    if (!response.ok) throw new Error("Network response was not ok");
    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    showToast("Gagal memuat data", "danger");
    return null;
  }
}

/**
 * Post Data
 */
async function postData(url, data) {
  const csrfToken = document
    .querySelector('meta[name="csrf-token"]')
    ?.getAttribute("content");
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Network response was not ok");
    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    showToast("Gagal mengirim data", "danger");
    return null;
  }
}

/**
 * Initialize Sidebar Collapse
 */
function initializeSidebarCollapse() {
  const collapseBtn = document.getElementById("sidebarCollapseBtn");
  const sidebar = document.querySelector(".sidebar");
  const mainContent = document.querySelector(".main-content");

  if (collapseBtn && sidebar) {
    collapseBtn.addEventListener("click", function () {
      // Toggle hidden (desktop) state - sidebar fully disappears
      sidebar.classList.toggle("hidden");
      collapseBtn.classList.toggle("open");
      const expanded = String(collapseBtn.classList.contains("open"));
      collapseBtn.setAttribute("aria-expanded", expanded);

      // Update aria-hidden for sidebar
      sidebar.setAttribute("aria-hidden", sidebar.classList.contains("hidden") ? "true" : "false");

      // Adjust main content margin
      if (sidebar.classList.contains("hidden")) {
        mainContent.style.marginLeft = "0";
      } else {
        mainContent.style.marginLeft = "20.00rem";
      }

      // Save state to localStorage (use new key 'sidebarHidden')
      localStorage.setItem(
        "sidebarHidden",
        sidebar.classList.contains("hidden")
      );
    });
  }

  // Load saved state (migrate old 'sidebarCollapsed' if present)
  const savedHidden = localStorage.getItem("sidebarHidden");
  const savedCollapsed = localStorage.getItem("sidebarCollapsed");
  const isHidden = savedHidden === "true" || (!savedHidden && savedCollapsed === "true");

  if (isHidden && sidebar) {
    sidebar.classList.add("hidden");
    sidebar.setAttribute("aria-hidden", "true");
    if (collapseBtn) {
      collapseBtn.classList.add("open");
      collapseBtn.setAttribute("aria-expanded", "true");
    }
    if (mainContent) {
      mainContent.style.marginLeft = "0";
    }
  }
}

/**
 * Smooth Scroll
 */
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});
