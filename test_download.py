#!/usr/bin/env python3
"""
Utility to test image downloads outside of the Flask app.
Run this directly to test if there are permission or configuration issues.
"""

import os
import sys
import requests
import uuid
from urllib.parse import urlparse

def test_download(url):
    print(f"Testing download from URL: {url}")
    
    # Create a test downloads directory
    download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_downloads')
    os.makedirs(download_dir, exist_ok=True)
    print(f"Download directory: {download_dir}")
    
    try:
        # Download the image
        print("Sending request...")
        response = requests.get(url, stream=True)
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {response.headers}")
        
        if response.status_code != 200:
            print(f"Error: Failed to download image. Status code: {response.status_code}")
            return False
        
        # Get filename from URL or generate a unique one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        print(f"Parsed filename: {filename}")
        
        # Clean up filename if it contains query parameters
        if '?' in filename:
            filename = filename.split('?')[0]
            
        if not filename:
            content_type = response.headers.get('content-type', '')
            ext = '.png'  # Default extension
            
            if 'image/jpeg' in content_type:
                ext = '.jpg'
            elif 'image/gif' in content_type:
                ext = '.gif'
            elif 'image/webp' in content_type:
                ext = '.webp'
                
            filename = f"{uuid.uuid4()}{ext}"
        
        # Save the file
        file_path = os.path.join(download_dir, filename)
        print(f"Saving to: {file_path}")
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Verify file exists
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"Success! File saved with size: {file_size} bytes")
            return True
        else:
            print(f"Error: File not found at {file_path}")
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_download.py <image_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    success = test_download(url)
    
    if success:
        print("Download test completed successfully!")
    else:
        print("Download test failed!")
    
    sys.exit(0 if success else 1)