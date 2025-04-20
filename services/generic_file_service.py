--- START OF FILE generic_file_service.py ---
import logging
import os
import magic  # python-magic library
from urllib.parse import urlparse

logger = logging.getLogger('discord_media_download')

def detect_file_type(file_path_or_url):
    """
    Detect file type using python-magic library (if available) or fallback to URL/extension.

    Args:
        file_path_or_url: Path to a local file or a URL.

    Returns:
        str: File type description (e.g., 'image/jpeg', 'video/mp4', 'application/octet-stream', 'unknown')
    """
    try:
        mime = magic.Magic(mime=True)
        if os.path.exists(file_path_or_url):
            file_type = mime.from_file(file_path_or_url)
            logger.debug(f"File type detected using python-magic (file): {file_type} for {file_path_or_url}")
            return file_type
        else:
            # If it's not a file path, assume it's a URL and try to get type from URL/extension
            parsed_url = urlparse(file_path_or_url)
            if parsed_url.path:
                filename = os.path.basename(parsed_url.path)
                if '.' in filename:
                    extension = filename.split('.')[-1].lower()
                    # Basic mapping, can be expanded
                    ext_to_type = {
                        'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
                        'png': 'image/png', 'gif': 'image/gif',
                        'mp4': 'video/mp4', 'webm': 'video/webm',
                        'pdf': 'application/pdf', 'zip': 'application/zip',
                        'txt': 'text/plain', 'html': 'text/html'
                    }
                    if extension in ext_to_type:
                        file_type = ext_to_type[extension]
                        logger.debug(f"File type inferred from URL extension: {file_type} for {file_path_or_url}")
                        return file_type

            logger.debug(f"Falling back to default file type 'application/octet-stream' for {file_path_or_url}")
            return 'application/octet-stream' # Default if no detection
    except ImportError:
        logger.warning("python-magic library not installed. File type detection might be less accurate.")
        # Fallback to basic URL/extension based detection if python-magic is not available
        parsed_url = urlparse(file_path_or_url)
        if parsed_url.path:
            filename = os.path.basename(parsed_url.path)
            if '.' in filename:
                extension = filename.split('.')[-1].lower()
                ext_to_type = { # Same basic mapping as above
                    'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
                    'png': 'image/png', 'gif': 'image/gif',
                    'mp4': 'video/mp4', 'webm': 'video/webm',
                    'pdf': 'application/pdf', 'zip': 'application/zip',
                    'txt': 'text/plain', 'html': 'text/html'
                }
                if extension in ext_to_type:
                    file_type = ext_to_type[extension]
                    logger.debug(f"File type inferred from URL extension (no magic): {file_type} for {file_path_or_url}")
                    return file_type

        logger.debug(f"Falling back to default file type 'application/octet-stream' (no magic fallback) for {file_path_or_url}")
        return 'application/octet-stream' # Default if no detection and no magic

    except Exception as e:
        logger.exception(f"Error detecting file type for {file_path_or_url}: {e}")
        return 'unknown'


def process_generic_file(file_path):
    """
    Process a generic file based on its detected type.
    This is a placeholder function for type-specific processing.

    Args:
        file_path: Path to the downloaded file.

    Returns:
        tuple: (success (bool), message (str))
    """
    file_type = detect_file_type(file_path)
    logger.info(f"Processing generic file of type: {file_type}, path: {file_path}")

    if file_type.startswith('image/'):
        logger.info(f"Detected image file: {file_path}")
        # Example: You could add image processing logic here (resizing, optimization etc.)
        # For now, just log a message.
        processing_message = "Image file detected, no specific image processing implemented yet."
        logger.info(processing_message)
        return True, processing_message

    elif file_type.startswith('video/'):
        logger.info(f"Detected video file: {file_path}")
        # Example: You could add video processing logic here (transcoding, thumbnail generation etc.)
        # For now, just log a message.
        processing_message = "Video file detected, no specific video processing implemented yet."
        logger.info(processing_message)
        return True, processing_message

    elif file_type == 'application/pdf':
        logger.info(f"Detected PDF file: {file_path}")
        processing_message = "PDF file detected, no specific PDF processing implemented yet."
        logger.info(processing_message)
        return True, processing_message

    elif file_type == 'text/plain':
        logger.info(f"Detected Text file: {file_path}")
        processing_message = "Text file detected, no specific text processing implemented yet."
        logger.info(processing_message)
        return True, processing_message

    else:
        logger.info(f"Detected other file type: {file_type} for {file_path}")
        processing_message = f"Detected file type: {file_type}, no specific processing for this type implemented."
        logger.info(processing_message)
        return True, processing_message


if __name__ == '__main__':
    # Example Usage (for testing purposes)
    logging.basicConfig(level=logging.DEBUG)

    # Test file type detection (you would need to create these dummy files or URLs)
    test_files_urls = [
        'test_image.jpg',  # Create a dummy jpg file
        'test_video.mp4',  # Create a dummy mp4 file
        'test_pdf.pdf',    # Create a dummy pdf file
        'document.txt',   # Create a dummy text file
        'https://example.com/image.png',
        'https://example.com/document.pdf',
        'https://example.com/unknown_file' # No extension
    ]

    for item in test_files_urls:
        file_type = detect_file_type(item)
        print(f"File/URL: {item}, Detected Type: {file_type}")

    # Example of processing a file (you would need to have downloaded a file first)
    # For demonstration, let's assume 'test_image.jpg' exists after download
    # if os.path.exists('test_image.jpg'):
    #     success, message = process_generic_file('test_image.jpg')
    #     print(f"Processing 'test_image.jpg' - Success: {success}, Message: {message}")