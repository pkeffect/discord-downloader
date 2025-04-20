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
    
    // Pagination variables
    let currentPage = 1;
    const itemsPerPage = 10;
    let totalFiles = 0;
    let filesList = [];
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const fileStartEl = document.getElementById('file-start');
    const fileEndEl = document.getElementById('file-end');
    const fileTotalEl = document.getElementById('file-total');
    const filesGrid = document.getElementById('files-grid');
    
    // Initialize pagination
    initPagination();
    
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
            
            // Reinitialize pagination after refresh
            initPagination();
            
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
    
    // Initialize pagination
    function initPagination() {
        // Get all file items
        const fileItems = document.querySelectorAll('.file-item');
        filesList = Array.from(fileItems);
        totalFiles = filesList.length;
        
        // Update total files count
        if (fileTotalEl) {
            fileTotalEl.textContent = totalFiles;
        }
        
        // Show first page
        updatePagination();
        
        // Setup pagination buttons
        if (prevPageBtn) {
            prevPageBtn.addEventListener('click', () => {
                if (currentPage > 1) {
                    currentPage--;
                    updatePagination();
                }
            });
        }
        
        if (nextPageBtn) {
            nextPageBtn.addEventListener('click', () => {
                const maxPages = Math.ceil(totalFiles / itemsPerPage);
                if (currentPage < maxPages) {
                    currentPage++;
                    updatePagination();
                }
            });
        }
    }
    
    // Update pagination display
    function updatePagination() {
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = Math.min(startIndex + itemsPerPage, totalFiles);
        
        // Update display counters
        if (fileStartEl && fileEndEl) {
            fileStartEl.textContent = totalFiles > 0 ? startIndex + 1 : 0;
            fileEndEl.textContent = endIndex;
        }
        
        // Hide all files
        filesList.forEach(file => {
            file.classList.add('hidden');
        });
        
        // Show only current page files
        for (let i = startIndex; i < endIndex; i++) {
            if (filesList[i]) {
                filesList[i].classList.remove('hidden');
            }
        }
        
        // Update buttons state
        if (prevPageBtn) {
            prevPageBtn.disabled = currentPage === 1;
        }
        
        if (nextPageBtn) {
            nextPageBtn.disabled = currentPage >= Math.ceil(totalFiles / itemsPerPage);
        }
    }
    
    // Load thumbnails for images
    function loadThumbnails() {
        const thumbnails = document.querySelectorAll('.thumbnail-container img');
        thumbnails.forEach(img => {
            const src = img.getAttribute('src');
            if (src) {
                // Check if file is an image
                const isImage = /\.(jpg|jpeg|png|gif|webp)$/i.test(src);
                if (isImage) {
                    img.style.display = 'block';
                } else {
                    img.style.display = 'none';
                }
            }
        });
    }
    
    // Load thumbnails on initial load
    loadThumbnails();
    
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