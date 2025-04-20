import os
import uuid
import logging
from config import DOWNLOAD_DIR

logger = logging.getLogger('discord_media_download')

def get_file_list():
    """
    Get list of files in the download directory.
    
    Returns:
        list: Sorted list of filenames in the download directory
    """
    if not os.path.exists(DOWNLOAD_DIR):
        logger.warning(f"Download directory does not exist: {DOWNLOAD_DIR}")
        return []
    
    try:
        files = sorted(os.listdir(DOWNLOAD_DIR))
        logger.debug(f"Found {len(files)} files in download directory")
        return files
    except Exception as e:
        logger.exception(f"Error listing files in download directory: {e}")
        return []

def save_file(content, filename):
    """
    Save binary content to a file in the download directory.
    
    Args:
        content: Binary content to save
        filename: Name of the file to save
    
    Returns:
        tuple: (success (bool), message (str), file_path (str))
    """
    try:
        # Check if file already exists and add numbering if needed
        file_path, filename = get_unique_filepath(filename)
        logger.info(f"Saving file to: {file_path}")
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Verify file was saved
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            logger.info(f"File saved successfully. Size: {file_size} bytes")
            return True, f"Media downloaded successfully as {filename}", file_path
        else:
            logger.error(f"File was not saved at {file_path}")
            return False, "File was not saved", None
            
    except Exception as e:
        logger.exception(f"Error saving file: {e}")
        return False, f"Error saving file: {str(e)}", None

def save_streamed_content(response, filename):
    """
    Save streamed content from a requests response object.
    
    Args:
        response: Requests response object with streaming content
        filename: Name of the file to save
    
    Returns:
        tuple: (success (bool), message (str), file_path (str))
    """
    try:
        # Check if file already exists and add numbering if needed
        file_path, filename = get_unique_filepath(filename)
        logger.info(f"Saving streamed content to: {file_path}")
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Verify file was saved
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            logger.info(f"File saved successfully. Size: {file_size} bytes")
            return True, f"Media downloaded successfully as {filename}", file_path
        else:
            logger.error(f"File was not saved at {file_path}")
            return False, "File was not saved", None
            
    except Exception as e:
        logger.exception(f"Error saving streamed content: {e}")
        return False, f"Error saving file: {str(e)}", None

def get_unique_filepath(filename):
    """
    Generates a unique filepath by adding sequential numbering if the file already exists.
    
    Args:
        filename: Original filename
    
    Returns:
        tuple: (unique_filepath, unique_filename)
    """
    base_path = os.path.join(DOWNLOAD_DIR, filename)
    
    # If file doesn't exist, return original
    if not os.path.exists(base_path):
        return base_path, filename
    
    # Get base name and extension
    base_name, ext = os.path.splitext(filename)
    
    # Try adding sequential numbers until we find an unused filename
    counter = 1
    while True:
        numbered_filename = f"{base_name}_{counter:03d}{ext}"
        numbered_path = os.path.join(DOWNLOAD_DIR, numbered_filename)
        
        if not os.path.exists(numbered_path):
            logger.debug(f"File already exists, using numbered filename: {numbered_filename}")
            return numbered_path, numbered_filename
        
        counter += 1

def generate_unique_filename(extension='.bin'):
    """
    Generate a unique filename with the given extension.
    
    Args:
        extension: File extension (default: .bin)
    
    Returns:
        str: Unique filename with extension
    """
    file_id = str(uuid.uuid4())
    logger.debug(f"Generated file ID: {file_id}")
    
    # Create the base filename
    base_filename = f"{file_id}{extension}"
    
    # Check if this filename already exists and make it unique if needed
    _, unique_filename = get_unique_filepath(base_filename)
    
    return unique_filename