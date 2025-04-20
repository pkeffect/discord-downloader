import re
import logging
import requests
from urllib.parse import urlparse
import os
from services.file_service import generate_unique_filename, save_streamed_content
from services.tenor_service import extract_tenor_gif_url

logger = logging.getLogger('discord_media_download')

def extract_url_from_html(html_content):
    """
    Extract media URL from HTML content.
    
    Args:
        html_content: HTML content that may contain embedded URLs
    
    Returns:
        str: Extracted media URL or original content if no URL found
    """
    logger.info("Attempting to extract direct URL from HTML content")
    
    # Look for data-safe-src attribute (Discord's direct media URL)
    safe_src_match = re.search(r'data-safe-src=["\']([^"\']+)["\']', html_content)
    
    if safe_src_match:
        # Found the direct media URL
        extracted_url = safe_src_match.group(1)
        logger.info(f"Extracted URL from HTML data-safe-src: {extracted_url}")
        return extracted_url
    
    # Try to find src attribute 
    src_match = re.search(r'src=["\']([^"\']+)["\']', html_content)
    if src_match:
        extracted_url = src_match.group(1)
        logger.info(f"Extracted URL from HTML src: {extracted_url}")
        return extracted_url
    
    # Try to find href as fallback
    href_match = re.search(r'href=["\']([^"\']+)["\']', html_content)
    if href_match:
        extracted_url = href_match.group(1)
        logger.info(f"Extracted href URL from HTML: {extracted_url}")
        
        # If this is a tenor link, follow it to get the actual GIF
        if 'tenor.com/view/' in extracted_url:
            logger.info(f"Found Tenor link, trying to extract direct media URL")
            try:
                # Try to extract the direct GIF URL from the Tenor page
                direct_url = extract_tenor_gif_url(extracted_url)
                if direct_url:
                    logger.info(f"Extracted direct media URL from Tenor: {direct_url}")
                    return direct_url
            except Exception as e:
                logger.error(f"Error extracting Tenor URL: {str(e)}")
        
        return extracted_url
    
    # If no URL found, return original content
    logger.warning("No URL found in HTML content")
    return html_content

def is_valid_media_url(url):
    """
    Check if the URL is valid and not a Discord channel link.
    
    Args:
        url: URL to validate
    
    Returns:
        tuple: (is_valid (bool), message (str))
    """
    # Check if this is a Discord channel link (not a media file)
    if ('discord.com/channels/' in url or 'discordapp.com/channels/' in url) and not any(
        ext in url.lower() for ext in ['.jpg', '.png', '.gif', '.webp', '.mp4']
    ):
        logger.warning(f"URL appears to be a Discord channel link, not a media file: {url}")
        return False, 'This appears to be a Discord channel link, not a media file. Please drag an image or GIF instead.'
    
    # Validate URL format
    parsed_url = urlparse(url)
    logger.debug(f"Parsed URL: {parsed_url}")
    
    if not parsed_url.scheme:
        logger.warning(f"URL has no scheme, cannot download: {url}")
        return False, 'Invalid URL format. Please drag a media file from Discord.'
    
    return True, 'Valid URL'

def determine_file_extension(content_type, url, original_filename=""):
    """
    Determine the appropriate file extension based on content type and URL.
    
    Args:
        content_type: Content type from response headers
        url: Source URL
        original_filename: Original filename, if available
    
    Returns:
        str: File extension with leading dot (e.g., '.jpg')
    """
    content_type = content_type.lower()
    logger.debug(f"Determining file extension for content type: {content_type}, URL: {url}")
    
    # Map content types to extensions
    content_type_map = {
        'image/jpeg': '.jpg',
        'image/jpg': '.jpg',
        'image/gif': '.gif',
        'image/png': '.png',
        'image/webp': '.webp',
        'video/mp4': '.mp4',
        'video/webm': '.webm',
        'text/html': '.html'
    }
    
    # Check content type first
    for ct, ext in content_type_map.items():
        if ct in content_type:
            logger.debug(f"Determined extension {ext} from content type")
            return ext
    
    # If content type doesn't provide extension, check URL
    url_lower = url.lower()
    
    # Discord-specific logic: URLs from Discord often end with .mp4 even for GIFs
    if 'discordapp.net' in url or 'discord.com' in url or 'cdn.discordapp.com' in url:
        if '.gif' in url_lower:
            logger.debug("Determined .gif extension from Discord URL")
            return '.gif'
        elif '.mp4' in url_lower:
            # Could be a GIF or MP4, let's use MP4 extension
            logger.debug("Determined .mp4 extension from Discord URL")
            return '.mp4'
        else:
            logger.debug("Using .bin as default extension for Discord content")
            return '.bin'  # Default for Discord content
    
    # Default extension based on URL hints for non-Discord URLs
    extensions = ['.gif', '.mp4', '.webm', '.webp', '.jpg', '.jpeg', '.png']
    for ext in extensions:
        if ext in url_lower:
            logger.debug(f"Determined {ext} extension from URL")
            return ext
    
    # Check original filename if provided
    if original_filename and '.' in original_filename:
        ext = f".{original_filename.split('.')[-1].lower()}"
        logger.debug(f"Using extension {ext} from original filename")
        return ext
    
    # Default case
    logger.debug("Using .bin as default extension")
    return '.bin'

def generate_filename(url, content_type):
    """
    Generate appropriate filename based on URL and content type.
    
    Args:
        url: Source URL
        content_type: Content type from response headers
    
    Returns:
        str: Generated filename
    """
    parsed_url = urlparse(url)
    
    # Try to get filename from URL path
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
        
        # If we have a valid filename, use it
        if original_filename and original_filename != '/':
            # Ensure proper extension based on content type
            file_ext = os.path.splitext(original_filename)[1].lower() if '.' in original_filename else ''
            content_ext = determine_file_extension(content_type, url)
            
            # If no extension or incorrect extension, append the correct one
            if not file_ext or file_ext != content_ext:
                # Remove existing extension if any
                base_name = original_filename.split('.')[0] if '.' in original_filename else original_filename
                filename = f"{base_name}{content_ext}"
                logger.debug(f"Updated filename with correct extension: {filename}")
                return filename
            
            # Return the original filename if extension is already correct
            return original_filename
    
    # If we couldn't get a filename from the URL, generate a unique one
    ext = determine_file_extension(content_type, url)
    return generate_unique_filename(ext)

def process_download(image_url):
    """
    Process download request for the given URL.
    
    Args:
        image_url: URL to download media from
    
    Returns:
        dict: Response with success status and message
    """
    logger.info(f"Processing download request for URL: {image_url}")
    
    if not image_url:
        logger.warning("No image URL provided")
        return {'success': False, 'message': 'No image URL provided.'}
    
    try:
        # Check if this is HTML content with embedded URLs (from Discord drag and drop)
        if image_url.startswith('<html>') or '<a ' in image_url:
            logger.info("Detected HTML content, attempting to extract direct URL")
            image_url = extract_url_from_html(image_url)
        
        # Validate URL
        valid, message = is_valid_media_url(image_url)
        if not valid:
            return {'success': False, 'message': message}
        
        # Download the image
        logger.info(f"Attempting to download from: {image_url}")
        response = requests.get(image_url, stream=True)
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")
        
        if response.status_code != 200:
            logger.error(f"Failed to download image. Status code: {response.status_code}")
            return {'success': False, 'message': f'Failed to download image. Status code: {response.status_code}'}
        
        # Get content type
        content_type = response.headers.get('content-type', '').lower()
        logger.debug(f"Content type: {content_type}")
        
        # Check for HTML content type which might indicate we didn't get a direct media URL
        if 'text/html' in content_type and not image_url.endswith('.html') and not 'video/mp4' in content_type:
            logger.warning(f"Received HTML content type for non-HTML URL: {image_url}")
            # Check if the URL points to a video hosting site
            if any(domain in image_url for domain in ['youtube.com', 'vimeo.com', 'dailymotion.com', 'discord.com']):
                # Let's try to process it as a video anyway
                logger.info(f"URL appears to be from a video site, attempting to process anyway: {image_url}")
            else:
                return {'success': False, 'message': 'Received HTML content instead of media. This may not be a direct media URL.'}
        
        # Generate appropriate filename
        filename = generate_filename(image_url, content_type)
        
        # Save the file
        success, message, _ = save_streamed_content(response, filename)
        
        return {'success': success, 'message': message}
        
    except Exception as e:
        logger.exception(f"Error downloading media: {str(e)}")
        return {'success': False, 'message': f'Error: {str(e)}'}