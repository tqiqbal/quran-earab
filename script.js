/*
 * Quran E'arab & Sarf - Shared Script
 */

document.addEventListener('DOMContentLoaded', () => {
    highlightActiveNav();
});

/**
 * Highlights the active navigation item based on the current URL
 */
function highlightActiveNav() {
    const currentPath = window.location.pathname;
    const page = currentPath.split('/').pop() || 'index.html';
    
    // Desktop Nav
    const desktopLinks = document.querySelectorAll('.nav-item');
    desktopLinks.forEach(link => {
        if (link.getAttribute('href') === page) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // Mobile Nav
    const mobileLinks = document.querySelectorAll('.bottom-nav-item');
    mobileLinks.forEach(link => {
        if (link.getAttribute('href') === page) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * Utility to show/hide loading state
 * @param {string} elementId - ID of the loading element
 * @param {boolean} show - Whether to show or hide
 */
function toggleLoading(elementId, show) {
    const el = document.getElementById(elementId);
    if (el) {
        if (show) {
            el.classList.remove('hidden');
            el.classList.add('show'); // For legacy support if needed
        } else {
            el.classList.add('hidden');
            el.classList.remove('show');
        }
    }
}

/**
 * Utility to show error message
 * @param {string} elementId - ID of the error element
 * @param {string} message - Error message to display
 */
function showError(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) {
        el.textContent = message;
        el.style.display = 'block';
        el.classList.remove('hidden');
    }
}
