// JavaScript for the index page of Discord Media Download

document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const dropArea = document.getElementById('drop-area');
    
    // Add active class when dragging over
    dropArea.addEventListener('dragenter', () => {
        dropArea.classList.add('active');
    });

    // Remove active class when dragging leaves
    dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('active');
    });

    // Prevent default behaviors
    dropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    // Handle drop event
    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        dropArea.classList.remove('active');
        
        const items = e.dataTransfer.items;
        for (let i = 0; i < items.length; i++) {
            if (items[i].kind === 'string') {
                items[i].getAsString((data) => {
                    console.log("Dropped data:", data);
                    
                    // Skip Discord channel links
                    if (data.includes('discord.com/channels/') && !data.includes('.jpg') && !data.includes('.png') && !data.includes('.gif') && !data.includes('.mp4')) {
                        showAlert('Discord channel links are not supported. Please drag an image or GIF instead.', 'error');
                        return;
                    }
                    
                    // Try to extract URL from HTML if it's HTML content
                    let url = data;
                    
                    // First look for data-safe-src attribute which contains direct media URL in Discord
                    const safeSrcMatch = data.match(/data-safe-src="([^"]+)"/);
                    if (safeSrcMatch && safeSrcMatch[1]) {
                        url = safeSrcMatch[1];
                        console.log("Extracted data-safe-src URL:", url);
                    } else {
                        // Try to find src attribute for images
                        const srcMatch = data.match(/src="([^"]+)"/);
                        if (srcMatch && srcMatch[1]) {
                            url = srcMatch[1];
                            console.log("Extracted src URL:", url);
                        } else {
                            // Try to find href as fallback
                            const hrefMatch = data.match(/href="([^"]+)"/);
                            if (hrefMatch && hrefMatch[1]) {
                                url = hrefMatch[1];
                                console.log("Extracted href URL:", url);
                            }
                        }
                    }
                    
                    // Send URL to server for download
                    console.log("Sending URL to server:", url);
                    downloadMedia(url);
                });
            } else {
                showAlert('Invalid item. Please drag an image or GIF from Discord.', 'error');
            }
        }
    });

    // Download the media
    function downloadMedia(url) {
        console.log("Attempting to download:", url);
        
        fetch('/download_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `image_url=${encodeURIComponent(url)}`
        })
        .then(response => {
            console.log("Server response status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("Server response data:", data);
            if (data.success) {
                showAlert(data.message, 'success');
            } else {
                showAlert(data.message, 'error');
            }
        })
        .catch((error) => {
            console.error("Fetch error:", error);
            showAlert('An error occurred while downloading the media.', 'error');
        });
    }
});