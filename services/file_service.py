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
        file_path = os.path.join(DOWNLOAD_DIR, filename)
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
        file_path = os.path.join(DOWNLOAD_DIR, filename)
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
    return f"{file_id}{extension}"