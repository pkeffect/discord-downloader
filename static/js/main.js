// Main JavaScript for Discord Media Download

// Show alert message
function showAlert(message, type) {
    const alert = document.getElementById('alert');
    const alertMessage = document.getElementById('alert-message');
    
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

// Close alert when the close button is clicked
document.addEventListener('DOMContentLoaded', function() {
    const closeAlertButton = document.querySelector('#alert button');
    if (closeAlertButton) {
        closeAlertButton.addEventListener('click', function() {
            document.getElementById('alert').style.display = 'none';
        });
    }
    
    // Update the current date and time in the footer
    updateDateTime();
    setInterval(updateDateTime, 60000); // Update every minute
});

// Update current date and time
function updateDateTime() {
    const datetimeElement = document.getElementById('current-datetime');
    if (datetimeElement) {
        const now = new Date();
        datetimeElement.textContent = now.toLocaleString();
    }
}

// Highlight active navigation item
document.addEventListener('DOMContentLoaded', function() {
    // Get current page path
    const currentPath = window.location.pathname;
    
    // Set the appropriate navigation link to active
    if (currentPath === '/') {
        document.getElementById('nav-home').classList.remove('text-gray-300');
        document.getElementById('nav-home').classList.add('text-blurple-500', 'font-medium');
    } else if (currentPath === '/debug') {
        document.getElementById('nav-debug').classList.remove('text-gray-300');
        document.getElementById('nav-debug').classList.add('text-blurple-500', 'font-medium');
    } else if (currentPath === '/logs') {
        document.getElementById('nav-logs').classList.remove('text-gray-300');
        document.getElementById('nav-logs').classList.add('text-blurple-500', 'font-medium');
    }
});

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}