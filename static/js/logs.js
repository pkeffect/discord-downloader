// JavaScript for the logs page of Discord Media Download

document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const logsContent = document.getElementById('logs');
    const refreshBtn = document.getElementById('refresh-btn');
    const autoRefreshBtn = document.getElementById('auto-refresh-btn');
    const clearLogsBtn = document.getElementById('clear-logs-btn');
    const logLevelFilter = document.getElementById('log-level-filter');
    const logSearch = document.getElementById('log-search');
    const autoRefreshIndicator = document.getElementById('auto-refresh-indicator');
    const lastRefreshSpan = document.getElementById('last-refresh');
    
    // Auto refresh settings
    let autoRefreshEnabled = true;
    let refreshInterval = 5000; // 5 seconds
    let refreshTimer;
    let originalLogs = '';
    
    // Store the original logs
    originalLogs = logsContent.innerHTML;
    
    // Highlight log levels
    highlightLogs();
    
    // Scroll to bottom
    scrollToBottom();
    
    // Start auto refresh
    startAutoRefresh();
    
    // Function to fetch logs
    async function fetchLogs() {
        try {
            const response = await fetch(window.location.href);
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            // Get the logs content
            const newLogs = doc.getElementById('logs').innerHTML;
            
            // Update logs if there's new content
            if (newLogs !== logsContent.innerHTML) {
                logsContent.innerHTML = newLogs;
                originalLogs = newLogs;
                
                // Apply current filters and highlighting
                applyFilters();
                highlightLogs();
                
                // Scroll to bottom if auto-scroll is enabled
                scrollToBottom();
            }
            
            // Update last refresh time
            const now = new Date();
            lastRefreshSpan.textContent = `Last refreshed: ${now.toLocaleTimeString()}`;
            
            // Animate refresh indicator
            autoRefreshIndicator.classList.add('auto-refresh-animation');
            setTimeout(() => {
                autoRefreshIndicator.classList.remove('auto-refresh-animation');
            }, 1000);
            
        } catch (error) {
            console.error('Error fetching logs:', error);
            lastRefreshSpan.textContent = `Last refresh failed: ${new Date().toLocaleTimeString()}`;
            autoRefreshIndicator.style.backgroundColor = '#ef4444'; // Red color
        }
    }
    
    // Function to highlight log levels
    function highlightLogs() {
        const text = logsContent.innerHTML;
        
        // Highlight log levels with colors
        const coloredText = text
            .replace(/\b(INFO)\b/g, '<span class="info">$1</span>')
            .replace(/\b(DEBUG)\b/g, '<span class="debug">$1</span>')
            .replace(/\b(WARNING)\b/g, '<span class="warning">$1</span>')
            .replace(/\b(ERROR)\b/g, '<span class="error">$1</span>')
            .replace(/\b(CRITICAL)\b/g, '<span class="critical">$1</span>');
        
        logsContent.innerHTML = coloredText;
    }
    
    // Function to apply filters
    function applyFilters() {
        const level = logLevelFilter.value;
        const searchText = logSearch.value.toLowerCase();
        
        // Reset to original logs
        let filteredText = originalLogs;
        
        // Apply level filter
        if (level !== 'all') {
            const lines = filteredText.split('\n');
            const filteredLines = lines.filter(line => {
                if (level === 'error' && (line.includes('ERROR') || line.includes('CRITICAL'))) {
                    return true;
                } else if (level === 'warning' && (line.includes('WARNING') || line.includes('ERROR') || line.includes('CRITICAL'))) {
                    return true;
                } else if (level === 'info' && (line.includes('INFO') || line.includes('WARNING') || line.includes('ERROR') || line.includes('CRITICAL'))) {
                    return true;
                }
                return false;
            });
            filteredText = filteredLines.join('\n');
        }
        
        // Apply search filter
        if (searchText) {
            const lines = filteredText.split('\n');
            const searchedLines = lines.filter(line => line.toLowerCase().includes(searchText));
            filteredText = searchedLines.join('\n');
        }
        
        logsContent.innerHTML = filteredText;
    }
    
    // Function to scroll to bottom
    function scrollToBottom() {
        const container = document.querySelector('.log-container');
        container.scrollTop = container.scrollHeight;
    }
    
    // Setup refresh button
    refreshBtn.addEventListener('click', () => {
        fetchLogs();
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
    
    // Setup clear logs button
    clearLogsBtn.addEventListener('click', () => {
        logsContent.innerHTML = '';
    });
    
    // Setup log level filter
    logLevelFilter.addEventListener('change', () => {
        applyFilters();
        highlightLogs();
    });
    
    // Setup log search
    logSearch.addEventListener('input', () => {
        applyFilters();
        highlightLogs();
    });
    
    // Start auto refresh
    function startAutoRefresh() {
        if (refreshTimer) clearInterval(refreshTimer);
        refreshTimer = setInterval(fetchLogs, refreshInterval);
    }
    
    // Stop auto refresh
    function stopAutoRefresh() {
        if (refreshTimer) clearInterval(refreshTimer);
    }
});