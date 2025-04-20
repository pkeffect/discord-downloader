from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import requests
from urllib.parse import urlparse
import uuid
import logging
import io
import datetime
import re
from tenor_handler import extract_tenor_gif_url

# Configure logging
log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_directory, exist_ok=True)

log_stream = io.StringIO()
file_handler = logging.FileHandler(os.path.join('downloads', 'app.log'))
stream_handler = logging.StreamHandler(log_stream)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        file_handler,
        stream_handler,
        logging.StreamHandler()  # Also log to console
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', template_folder='templates')

# Create static directories if they don't exist
for directory in ['static/js', 'static/css']:
    os.makedirs(directory, exist_ok=True)

# Create download directory if it doesn't exist
DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
logger.info(f"Download directory set to: {DOWNLOAD_DIR}")

# Create the server-side include function to handle template inclusion
def include_template(template_name):
    return render_template(template_name)

# Register the function with Jinja2
app.jinja_env.globals.update(include_template=include_template)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_image', methods=['POST'])
def download_image():
    image_url = request.form.get('image_url')
    logger.info(f"Received download request for URL: {image_url}")
    
    if not image_url:
        logger.warning("No image URL provided")
        return jsonify({'success': False, 'message': 'No image URL provided.'})
    
    try:
        # Check if this is HTML content with embedded URLs (from Discord drag and drop)
        if image_url.startswith('<html>') or '<a ' in image_url:
            logger.info("Detected HTML content, attempting to extract direct URL")
            
            # Look for data-safe-src attribute (Discord's direct media URL)
            safe_src_match = re.search(r'data-safe-src=["\']([^"\']+)["\']', image_url)
            
            if safe_src_match:
                # Found the direct media URL
                extracted_url = safe_src_match.group(1)
                logger.info(f"Extracted URL from HTML data-safe-src: {extracted_url}")
                image_url = extracted_url
            else:
                # Try to find src attribute 
                src_match = re.search(r'src=["\']([^"\']+)["\']', image_url)
                if src_match:
                    extracted_url = src_match.group(1)
                    logger.info(f"Extracted URL from HTML src: {extracted_url}")
                    image_url = extracted_url
                else:
                    # Try to find href as fallback
                    href_match = re.search(r'href=["\']([^"\']+)["\']', image_url)
                    if href_match:
                        extracted_url = href_match.group(1)
                        logger.info(f"Extracted href URL from HTML: {extracted_url}")
                        
                        # If this is a tenor link, we need to follow it to get the actual GIF
                        if 'tenor.com/view/' in extracted_url:
                            logger.info(f"Found Tenor link, trying to extract direct media URL")
                            try:
                                # Try to extract the direct GIF URL from the Tenor page
                                direct_url = extract_tenor_gif_url(extracted_url)
                                if direct_url:
                                    logger.info(f"Extracted direct media URL from Tenor: {direct_url}")
                                    image_url = direct_url
                                else:
                                    # Otherwise, just use the tenor view URL
                                    image_url = extracted_url
                            except Exception as e:
                                logger.error(f"Error extracting Tenor URL: {str(e)}")
                                image_url = extracted_url
                        else:
                            image_url = extracted_url
        
        # If this is a Discord URL, check if it points to a channel instead of a media file
        if ('discord.com/channels/' in image_url or 'discordapp.com/channels/' in image_url) and not ('.jpg' in image_url.lower() or '.png' in image_url.lower() or '.gif' in image_url.lower() or '.webp' in image_url.lower() or '.mp4' in image_url.lower()):
            logger.warning(f"URL appears to be a Discord channel link, not a media file: {image_url}")
            return jsonify({'success': False, 'message': 'This appears to be a Discord channel link, not a media file. Please drag an image or GIF instead.'})
            
        # Accept any URL - we'll download from anywhere
        parsed_url = urlparse(image_url)
        logger.debug(f"Parsed URL: {parsed_url}")
        
        if not parsed_url.scheme:
            logger.warning(f"URL has no scheme, cannot download: {image_url}")
            return jsonify({'success': False, 'message': 'Invalid URL format. Please drag a media file from Discord.'})
        
        # Download the image
        logger.info(f"Attempting to download from: {image_url}")
        response = requests.get(image_url, stream=True)
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        
        if response.status_code != 200:
            logger.error(f"Failed to download image. Status code: {response.status_code}")
            return jsonify({'success': False, 'message': f'Failed to download image. Status code: {response.status_code}'})
        
        # Determine file extension from content type or URL
        content_type = response.headers.get('content-type', '').lower()
        logger.debug(f"Content type: {content_type}")
        
        # Get the original filename or use the last part of the path
        if parsed_url.path:
            original_filename = os.path.basename(parsed_url.path)
            # Clean up filename if it contains query parameters
            if '?' in original_filename:
                original_filename = original_filename.split('?')[0]
            logger.debug(f"Original filename from URL path: {original_filename}")
            
            # Discord CDN URLs often have filenames like "image0.jpg" which aren't very descriptive
            # For better filenames, we can use the containing folder name + the filename
            if ('cdn.discordapp.com' in parsed_url.netloc or 'media.discordapp.net' in parsed_url.netloc) and 'attachments/' in parsed_url.path:
                try:
                    # Path typically looks like: /attachments/SERVER_ID/MESSAGE_ID/filename.ext
                    path_parts = parsed_url.path.split('/')
                    if len(path_parts) >= 4:  # Make sure we have enough parts
                        message_id = path_parts[-2]  # Get the message ID
                        filename_part = path_parts[-1]  # Get the filename part
                        # If it's a generic name like "image0.jpg", use the message ID to make it unique
                        if filename_part.startswith('image') and filename_part[5].isdigit():
                            ext = os.path.splitext(filename_part)[1]  # Get the extension
                            new_filename = f"discord_{message_id}{ext}"
                            logger.debug(f"Using Discord message ID in filename: {new_filename}")
                            original_filename = new_filename
                except Exception as e:
                    logger.exception(f"Error processing Discord filename: {e}")
                    # Keep the original filename if there's an error
        else:
            original_filename = ""
        
        # Check if we need to generate a filename
        if not original_filename or original_filename == '/':
            # Generate a unique ID
            file_id = str(uuid.uuid4())
            logger.debug(f"Generated file ID: {file_id}")
            
            # Determine extension based on content type
            if 'image/jpeg' in content_type or 'image/jpg' in content_type:
                ext = '.jpg'
            elif 'image/gif' in content_type:
                ext = '.gif'
            elif 'image/png' in content_type:
                ext = '.png'
            elif 'image/webp' in content_type:
                ext = '.webp'
            elif 'video/mp4' in content_type:
                ext = '.mp4'
            elif 'video/webm' in content_type:
                ext = '.webm'
            elif 'text/html' in content_type:
                ext = '.html'  # This should be rare if URL extraction works
            else:
                # Discord-specific logic: URLs from Discord often end with .mp4 even for GIFs
                if 'discordapp.net' in image_url or 'discord.com' in image_url or 'cdn.discordapp.com' in image_url:
                    if '.gif' in image_url.lower():
                        ext = '.gif'
                    elif '.mp4' in image_url.lower():
                        # Could be a GIF or MP4, let's use MP4 extension
                        ext = '.mp4'
                    else:
                        ext = '.bin'  # Default for Discord content
                else:
                    # Default extension based on URL hints for non-Discord URLs
                    if '.gif' in image_url.lower():
                        ext = '.gif'
                    elif '.mp4' in image_url.lower():
                        ext = '.mp4'
                    elif '.webm' in image_url.lower():
                        ext = '.webm'
                    elif '.webp' in image_url.lower():
                        ext = '.webp'
                    elif '.jpg' in image_url.lower() or '.jpeg' in image_url.lower():
                        ext = '.jpg'
                    elif '.png' in image_url.lower():
                        ext = '.png'
                    else:
                        # Default case
                        ext = '.bin'
            
            filename = f"{file_id}{ext}"
            logger.debug(f"Generated filename: {filename}")
        else:
            # We have an original filename, but we might need to fix the extension
            filename = original_filename
            
            # Check if we need to add or fix extension based on content type
            # This is especially important for Discord URLs that might not have the correct extension
            file_ext = None
            if '.' in filename:
                file_ext = filename.split('.')[-1].lower()
            
            # Apply correct extension based on content type
            if 'image/jpeg' in content_type or 'image/jpg' in content_type:
                if not file_ext or file_ext not in ['jpg', 'jpeg']:
                    filename = f"{filename.split('.')[0]}.gif"
                logger.debug(f"Changed extension to gif based on URL: {filename}")
                
        # Final check to ensure we have a valid extension
        if '.' not in filename:
            logger.warning(f"No file extension detected for: {filename}, URL: {image_url}")
            return jsonify({'success': False, 'message': 'Could not determine file type. Please try a different file.'})
            
        logger.debug(f"Final filename: {filename}")
        
        # Save the file
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        logger.info(f"Saving file to: {file_path}")
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Verify file was saved
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            logger.info(f"File saved successfully. Size: {file_size} bytes")
            return jsonify({
                'success': True, 
                'message': f'Media downloaded successfully as {filename}'
            })
        else:
            logger.error(f"File was not saved at {file_path}")
            return jsonify({'success': False, 'message': 'File was not saved'})
        
    except Exception as e:
        logger.exception(f"Error downloading media: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})"{filename.split('.')[0]}.jpg"
                    logger.debug(f"Changed extension to jpg: {filename}")
            elif 'image/gif' in content_type:
                if not file_ext or file_ext != 'gif':
                    filename = f"{filename.split('.')[0]}.gif"
                    logger.debug(f"Changed extension to gif: {filename}")
            elif 'image/png' in content_type:
                if not file_ext or file_ext != 'png':
                    filename = f"{filename.split('.')[0]}.png"
                    logger.debug(f"Changed extension to png: {filename}")
            elif 'image/webp' in content_type:
                if not file_ext or file_ext != 'webp':
                    filename = f"{filename.split('.')[0]}.webp"
                    logger.debug(f"Changed extension to webp: {filename}")
            elif 'video/mp4' in content_type:
                if not file_ext or file_ext != 'mp4':
                    filename = f"{filename.split('.')[0]}.mp4"
                    logger.debug(f"Changed extension to mp4: {filename}")
            elif 'video/webm' in content_type:
                if not file_ext or file_ext != 'webm':
                    filename = f"{filename.split('.')[0]}.webm"
                    logger.debug(f"Changed extension to webm: {filename}")
            elif 'text/html' in content_type and not original_filename.endswith('.html'):
                # Don't download HTML content unless it's explicitly requested
                logger.warning(f"Received HTML content type for non-HTML URL: {image_url}")
                return jsonify({'success': False, 'message': 'Received HTML content instead of media. This may not be a direct media URL.'})
            # Discord-specific handling for animated content
            elif '.mp4' in image_url.lower() and (not file_ext or file_ext != 'mp4'):
                # For animated content from Discord that's served as MP4
                filename = f"{filename.split('.')[0]}.mp4"
                logger.debug(f"Changed extension to mp4 based on URL: {filename}")
            elif '.gif' in image_url.lower() and (not file_ext or file_ext != 'gif'):
                filename = f