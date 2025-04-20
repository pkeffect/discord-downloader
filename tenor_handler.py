import re
import requests
import logging

logger = logging.getLogger(__name__)

def extract_tenor_gif_url(tenor_url):
    """
    Extracts the direct GIF URL from a Tenor link
    
    Args:
        tenor_url: A URL like https://tenor.com/view/something
        
    Returns:
        Direct URL to the GIF or None if not found
    """
    logger.info(f"Attempting to extract GIF from Tenor URL: {tenor_url}")
    
    try:
        # GET the tenor page
        response = requests.get(tenor_url)
        if response.status_code != 200:
            logger.error(f"Failed to fetch Tenor page. Status code: {response.status_code}")
            return None
            
        # Look for GIF URL in the page content
        html_content = response.text
        
        # Option 1: Look for contentUrl in JSON-LD
        json_ld_match = re.search(r'"contentUrl":\s*"(https://media\.tenor\.com/[^"]+\.gif)"', html_content)
        if json_ld_match:
            gif_url = json_ld_match.group(1)
            logger.info(f"Found GIF URL in JSON-LD: {gif_url}")
            return gif_url
            
        # Option 2: Look for og:image meta tag
        og_image_match = re.search(r'<meta property="og:image" content="([^"]+)"', html_content)
        if og_image_match:
            image_url = og_image_match.group(1)
            logger.info(f"Found image URL in og:image: {image_url}")
            # Convert to GIF URL if needed
            if not image_url.endswith('.gif'):
                # Try to convert to GIF URL format
                if '/view/' in tenor_url:
                    gif_id = tenor_url.split('/view/')[1].split('-')[-1]
                    if gif_id.isdigit():
                        # Construct potential GIF URL
                        gif_url = f"https://media.tenor.com/images/{gif_id}/tenor.gif"
                        logger.info(f"Constructed GIF URL from ID: {gif_url}")
                        return gif_url
            return image_url
            
        # Option 3: Look for video URL if GIF not found
        video_match = re.search(r'<meta property="og:video" content="([^"]+)"', html_content)
        if video_match:
            video_url = video_match.group(1)
            logger.info(f"Found video URL in og:video: {video_url}")
            return video_url
            
        # Option 4: Direct search for any media files
        media_match = re.search(r'(https://media\.tenor\.com/[^"\']+\.(gif|mp4|webm))', html_content)
        if media_match:
            media_url = media_match.group(0)
            logger.info(f"Found media URL with regex: {media_url}")
            return media_url
            
        logger.warning("No GIF URL found in Tenor page")
        return None
        
    except Exception as e:
        logger.exception(f"Error extracting Tenor GIF URL: {e}")
        return None