// JavaScript for the debug page of Discord Media Download

document.addEventListener('DOMContentLoaded', function() {
    // Auto refresh functionality
    let autoRefreshEnabled = true;
    let refreshInterval = 5000; // 5 seconds
    let refreshTimer;
    const refreshBtn = document.getElementById('refresh-btn');
    const autoRefreshBtn = document.getElementById('auto-refresh-btn');
    const autoRefreshIndicator = document.getElementById('auto-refresh-indicator');
    const lastRefreshSpan = document.getElementById('last-refresh');
    
    // Function to fetch debug data
    async function fetchDebugData() {
        try {
            const response = await fetch(window.location.href);
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Extract the debug content from the fetched HTML
            const newDebugContent = doc.getElementById('debug-content').innerHTML;
            document.getElementById('debug-content').innerHTML = newDebugContent;
            
            // Update last refresh time
            const now = new Date();
            lastRefreshSpan.textContent = `Last refreshed: ${now.toLocaleTimeString()}`;
            
            // Add and remove pulse animation
            autoRefreshIndicator.classList.add('auto-refresh-animation');
            setTimeout(() => {
                autoRefreshIndicator.classList.remove('auto-refresh-animation');
            }, 1000);
            
        } catch (error) {
            console.error('Error fetching debug data:', error);
            lastRefreshSpan.textContent = `Last refresh failed: ${new Date().toLocaleTimeString()}`;
            autoRefreshIndicator.classList.remove('auto-refresh-animation');
            autoRefreshIndicator.style.backgroundColor = '#ef4444'; // Red color
        }
    }
    
    // Setup refresh button
    refreshBtn.addEventListener('click', () => {
        fetchDebugData();
    });
    
    // Setup auto refresh button
    autoRefreshBtn.addEventListener('click', () => {
        autoRefreshEnabled = !autoRefreshEnabled;
        
        if (autoRefreshEnabled) {
            autoRefreshBtn.textContent = 'Auto Refresh: ON';
            autoRefreshBtn.classList.remove('bg-gray-600', 'hover:bg-gray-500');
            autoRefreshBtn.classList.add('bg-green-600', 'hover:bg-green-500');
            autoRefreshIndicator.style.backgroundColor = '#22c55e'; // Green color
            startAutoRefresh();
        } else {
            autoRefreshBtn.textContent = 'Auto Refresh: OFF';
            autoRefreshBtn.classList.remove('bg-green-600', 'hover:bg-green-500');
            autoRefreshBtn.classList.add('bg-gray-600', 'hover:bg-gray-500');
            autoRefreshIndicator.style.backgroundColor = '#6b7280'; // Gray color
            stopAutoRefresh();
        }
    });
    
    // Start auto refresh
    function startAutoRefresh() {
        if (refreshTimer) clearInterval(refreshTimer);
        refreshTimer = setInterval(fetchDebugData, refreshInterval);
    }
    
    // Stop auto refresh
    function stopAutoRefresh() {
        if (refreshTimer) clearInterval(refreshTimer);
    }
    
    // Initialize auto refresh
    startAutoRefresh();
});