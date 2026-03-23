/* =============================================
   PYNANCE — main.js  (shared across all pages)
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {

  /* ---- Active Nav Link ---- */
  const currentFile = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link[data-page]').forEach(link => {
    if (link.dataset.page === currentFile) {
      link.classList.add('active');
    }
  });

  /* ---- User Dropdown ---- */
  const avatarBtn = document.getElementById('avatarBtn');
  const userDropdown = document.getElementById('userDropdown');

  if (avatarBtn && userDropdown) {
    avatarBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      userDropdown.classList.toggle('open');
    });

    document.addEventListener('click', () => {
      userDropdown.classList.remove('open');
    });
  }

  /* ---- Mobile Sidebar ---- */
  const hamburger = document.getElementById('hamburger');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');

  if (hamburger && sidebar) {
    hamburger.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      overlay && overlay.classList.toggle('active');
    });
  }

  if (overlay) {
    overlay.addEventListener('click', () => {
      sidebar && sidebar.classList.remove('open');
      overlay.classList.remove('active');
    });
  }

  /* ---- Toast Helper ---- */
  window.showToast = function(message) {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 2900);
  };

});
