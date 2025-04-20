// Main JavaScript for Discord Media Download

// Wait for DOM and stylesheets to be fully loaded
window.addEventListener('load', function() {
    // This will only run after all resources (DOM, CSS, images) are fully loaded
    initializeUI();
});

// Initialize UI elements
function initializeUI() {
    // Set up alert close button
    const closeAlertButton = document.querySelector('#alert button');
    if (closeAlertButton) {
        closeAlertButton.addEventListener('click', function() {
            document.getElementById('alert').style.display = 'none';
        });
    }
    
    // Update the current date and time in the footer
    updateDateTime();
    setInterval(updateDateTime, 60000); // Update every minute
    
    // Highlight active navigation item
    highlightNavigation();
    
    // Prevent default drag behaviors
    preventDefaultDrag();
}

// Show alert message
function showAlert(message, type) {
    const alert = document.getElementById('alert');
    const alertMessage = document.getElementById('alert-message');
    
    if (!alert || !alertMessage) return;
    
    alertMessage.textContent = message;
    alert.className = `fixed top-20 left-1/2 transform -translate-x-1/2 px-4 py-3 rounded-lg text-white font-semibold flex items-center shadow-lg ${type === 'success' ? 'bg-green-600' : 'bg-red-600'}`;
    alert.style.display = 'flex';
    
    // Also log to console for debugging
    if (type === 'success') {
        console.log("SUCCESS:", message);
    } else {
        console.error("ERROR:", message);
    }
    
    // Clear any existing timeout
    if (window.alertTimeout) {
        clearTimeout(window.alertTimeout);
        window.alertTimeout = null;
    }
    
    // Only auto-hide success messages
    if (type === 'success') {
        window.alertTimeout = setTimeout(() => {
            alert.style.display = 'none';
        }, 5000);
    }
    // Error messages remain visible until manually closed by the X button
}

// Update current date and time
function updateDateTime() {
    const datetimeElement = document.getElementById('current-datetime');
    if (datetimeElement) {
        const now = new Date();
        datetimeElement.textContent = now.toLocaleString();
    }
}

// Highlight active navigation item
function highlightNavigation() {
    // Get current page path
    const currentPath = window.location.pathname;
    
    // Set the appropriate navigation link to active
    if (currentPath === '/') {
        const navHome = document.getElementById('nav-home');
        if (navHome) {
            navHome.classList.remove('text-gray-300');
            navHome.classList.add('text-blurple-500', 'font-medium');
        }
    } else if (currentPath === '/debug') {
        const navDebug = document.getElementById('nav-debug');
        if (navDebug) {
            navDebug.classList.remove('text-gray-300');
            navDebug.classList.add('text-blurple-500', 'font-medium');
        }
    } else if (currentPath === '/logs') {
        const navLogs = document.getElementById('nav-logs');
        if (navLogs) {
            navLogs.classList.remove('text-gray-300');
            navLogs.classList.add('text-blurple-500', 'font-medium');
        }
    }
}

// Prevent default drag behaviors
function preventDefaultDrag() {
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        document.body.addEventListener(eventName, function(e) {
            e.preventDefault();
            e.stopPropagation();
        }, false);
    });
}

// Make functions globally available
window.showAlert = showAlert;