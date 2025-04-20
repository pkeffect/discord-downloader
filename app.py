

``` <!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Discord Image Downloader</title> <script src="https://cdn.tailwindcss.com"></script> <script> tailwind.config = {

pasted

can we combine these or somehow set them up to run in docker, im not sure how flask works but i know a lot of servers use uvicorn for easy docker setups. i do not want to loose any functionality, so if there is a better way to do this i would like recommendations. we need to be able to run the container and go to the specified port in our browser and be greeted with the index.html and it shold be able to accept media dragged from discord to it and download it from whereever the originating link s from. it should stay simple as we can for now and can expand later if needed. we just need it to function first as a docker container then we can expand. thank you

I'll help you set up a Docker container that runs your Discord Image Downloader application. Looking at your HTML file, I can see it has a client-side interface but needs a server component to handle the image downloads. Let's create a complete solution with Flask and package it in Docker.

First, let's create a Flask application that will serve your HTML and handle the image downloads:


app.py
Code 
Now, let's create the proper directory structure and move your HTML file to the templates folder:


templates/index.html
Code 
Now, let's create a requirements.txt file for the Python dependencies:


requirements.txt
Code 
Let's create the Dockerfile:


Dockerfile
Code 
Now let's create a docker-compose.yml file to make it easier to run the container:


docker-compose.yml
Code 
Finally, let's create a README.md file with instructions on how to use this container:


README.md
Document 
Let's also create a .dockerignore file to optimize the build process:


.dockerignore
Code 
Project Overview
I've created a complete Docker setup for your Discord Image Downloader. Here's what I've done:

Flask Application (app.py):
Set up a Flask server that serves the web interface
Created an endpoint to handle image downloads
Added validation to ensure only Discord images are processed
Implemented proper file handling with unique filenames
Directory Structure:
Organized the app with templates for HTML
Added a downloads directory where images will be saved
Docker Configuration:
Created a Dockerfile based on Python 3.9-slim
Added a docker-compose.yml for easy deployment
Set up volume mounting so downloads persist outside the container
Added proper port exposure (5000)
Documentation:
Comprehensive README with instructions
Alternative deployment options including Uvicorn
How to Use
Place all these files in the same directory structure:
discord-image-downloader/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── README.md
└── templates/
    └── index.html
Open a terminal in that directory and run:
bash
docker-compose up -d
Access the application at http://localhost:5000
Drag and drop images from Discord to download them
Improvements Made
Extended Discord URL Support: Added support for media.discordapp.net URLs which are sometimes used by Discord
File Type Detection: The app now properly detects file types and assigns the correct extension
Persistent Storage: Using Docker volumes to keep downloads available after container restarts
Error Handling: Better error messages and validation
Alternative with Uvicorn
If you prefer using Uvicorn as mentioned in your requirements, I've included instructions in the README. It's a simple change to the Dockerfile and requirements.txt.

Would you like me to make any adjustments to this setup?




Said only discord images are able to be downloaded....

172.22.0.1 - - [20/Apr/2025 14:07:26] "POST /download_image HTTP/1.1" 200 -

172.22.0.1 - - [20/Apr/2025 14:07:26] "POST /download_image HTTP/1.1" 200 -

thats in the log an nothing downloaded, could use more logging and debugging, I know for a fact to that the original code worked flawlessly before we dockerized it.

I see the issue. You're right that the logs show requests are being processed but no images are being downloaded. Let's add more debugging and fix the validation that's too restrictive. The original code likely worked because it was handling the URLs correctly, but our Docker implementation might have issues.

Let's update the app.py file with better logging and less restrictive URL validation:


app.py
Code ∙ Version 2 
Now, let's update the index.html template to be more permissive with URLs and add more debugging information:


templates/index.html
Code ∙ Version 2 
Let's update the docker-compose.yml file to expose the logs more clearly:


docker-compose.yml
Code ∙ Version 2 
Now let's add a simple debug/status page to help with troubleshooting:


app.py
Code ∙ Version 3 
Let's create a debug.html template:


templates/debug.html
Code 
Finally, let's add a test utility to help diagnose Docker permission issues:


test_download.py
Code 
Let's update the Dockerfile to ensure proper permissions:


Dockerfile
Code ∙ Version 2 
Now, let's update the README with the debugging instructions:


README.md
Document ∙ Version 2 
Fixes and Improvements
I've made several important changes to fix the issues with the Docker setup:

1. Fixed URL Validation
The main issue was that the app was too restrictive about what URLs it would accept. I've made these changes:

Removed URL validation entirely on the server side
Updated the frontend to accept any URL, not just Discord URLs
Added thorough logging to track what's happening with each request
2. Added Debugging Capabilities
I've added several tools to help diagnose issues:

Enhanced Logging: Detailed logs at each step of the download process
Debug Page: A web page at http://localhost:5000/debug showing system info and downloaded files
Test Utility: A standalone script (test_download.py) to test downloading outside the Flask app
3. Fixed Permission Issues
Docker containers often have permission problems with mounted volumes:

Added explicit permissions (chmod 777) for the downloads directory
Updated docker-compose.yml to ensure logs are properly captured
Added instructions for fixing permissions manually if needed
4. Improved Docker Configuration
Added curl to the container for network debugging
Made sure PYTHONUNBUFFERED is set for better logging
Configured proper log rotation
5. Better Error Handling
Added verification that files are actually being saved
Enhanced error messages with more details
Added file size reporting to confirm successful downloads
How to Deploy the Fixed Version
Replace all your existing files with these updated versions
Make sure your downloads directory has the right permissions:
bash
mkdir -p downloads
chmod 777 downloads
Rebuild and restart the container:
bash
docker-compose down
docker-compose build
docker-compose up -d
Check the logs for any errors:
bash
docker-compose logs -f
Access the debug page at http://localhost:5000/debug to verify the system configuration
If you're still having issues, run the test script:
bash
docker exec -it discord_image_downloader python test_download.py https://example.com/image.jpg
These changes should resolve the downloading issues while maintaining all the original functionality. The application is now more robust and provides better tools for troubleshooting.




File "/app/app.py", line 118

app.run(host='0.0.0.0', port=5000, debug=True)from flask import Flask, request, jsonify, render_template, send_from_directory

^^^^

SyntaxError: invalid syntax

File "/app/app.py", line 118

app.run(host='0.0.0.0', port=5000, debug=True)from flask import Flask, request, jsonify, render_template, send_from_directory

^^^^

I see the problem - there's a syntax error in the app.py file. Let me fix that right away.


app.py
Code ∙ Version 4 
I fixed the syntax error in the app.py file. It looks like there was an issue where some code was accidentally inserted into the last line, causing the syntax error.

Now let's rebuild the Docker container with the fixed code:

First, stop your current container if it's running:
bash
docker-compose down
Rebuild the container with the fixed code:
bash
docker-compose build
Start the container again:
bash
docker-compose up -d
Check the logs to make sure it's starting correctly:
bash
docker-compose logs -f
After these steps, your Docker container should start properly with the fixed app.py file. The application should now work as expected, allowing you to drag and drop images from Discord and download them.

If you're still experiencing issues, here are a few things to check:

Verify that the downloads directory exists and has the correct permissions
Visit the debug page at http://localhost:5000/debug to check the system configuration
Try using the test_download.py script to isolate any downloading issues
Is there anything specific about the error that you'd like me to explain or any other issues you're encountering?




kinda works but none of the console is going to the logs, need more debugging because errors pop up in a red bubble real fast and disappear before i can read them, they need to stay longer, but normal image download worked, when i saved an animated gid it grabbed the file but left off the ,gif file extension

Let me address these issues to improve the user experience and fix the file extension problem.

First, let's fix the error notification duration and make sure it stays visible longer:


templates/index.html
Code ∙ Version 3 
Now let's update the app.py file to fix the file extension issue and improve logging:


app.py
Code ∙ Version 5 
Let's also update the Dockerfile to properly output logs to stdout/stderr:


Dockerfile
Code ∙ Version 3 
Now let's add a log view directly in the UI so you can see errors right in the browser:


app.py
Code ∙ Version 6 
Now let's add a logs route to the app.py file:


app.py
Code ∙ Version 7 
Now let's create a logs template:


templates/logs.html
Code 
Let's also update the index.html to add a link to the logs page:


templates/index.html
Code ∙ Version 4 
Let's add more debugging to the browser console too:


templates/index.html
Code ∙ Version 5 
Now let's update the README with information about the new features:


README.md
Document ∙ Version 3 
Let's rebuild the Docker container to apply all these changes:

Rebuild and restart the container:
bash
docker-compose down
docker-compose build
docker-compose up -d
Summary of Changes
I've made several important improvements to fix the issues you mentioned:

1. Fixed File Extension Issues
I've completely overhauled the file extension handling:

Now properly checks content-type headers
Adds the correct extension for animated GIFs and other image types
Preserves original filename when possible, but ensures proper extension
2. Improved Error Notifications
I've made the error notifications much more helpful:

Errors now stay visible for 10 seconds (success messages for 5 seconds)
Removed the fade-out animation that was hiding errors too quickly
All error messages are now also logged to browser console
3. Added In-Browser Logging
I've added a complete logging system that's accessible right in your browser:

Go to http://localhost:5000/logs to see all application logs
Color-coded log levels for easier reading
Updates when you refresh the page
Logs are also saved to the downloads folder as app.log
4. Enhanced Browser Console Debugging
Added detailed console.log messages for each step of the process
Shows the exact URL being processed
Displays the server's response in detail
5. Improved Docker Configuration
Set the Python unbuffered mode to ensure logs appear immediately
Added proper configuration for log file storage
How to Use the New Features
Debug Page: Access at http://localhost:5000/debug
Shows system information
Lists all downloaded files
Shows environment variables
Logs Page: Access at http://localhost:5000/logs
Shows detailed application logs
Color-coded by log level
Updates when refreshed
Browser Console: Open browser DevTools (F12)
See detailed debug information
Track each step of the download process
These changes should make it much easier to identify and fix any remaining issues with the application. The logs will show exactly what's happening during the download process, and the improved error notifications will give you time to read any error messages.





2025-04-20 14:22:54,699 - __main__ - INFO - Download directory set to: /app/downloads 2025-04-20 14:22:54,702 - __main__ - INFO - Starting Discord Image Downloader app... 2025-04-20 14:22:54,729 - werkzeug - INFO - [31m[1mWARNING: This is a development server. Do not use it in a production deploym

pasted

it is not downloading anything correctly now..sigh ... maybe this was a bad idea

I see the issue from the logs. You're right that it's not downloading correctly - it's getting HTML pages instead of the actual GIF/video files. The problem is with how Discord provides the media URLs.

When you drag content from Discord, it's sending HTML snippet with links rather than the direct media URL. Let's fix that by extracting the actual media URL from the HTML.


app.py
Code ∙ Version 8 
Now let's update the frontend to also extract the URL from the HTML snippet:


templates/index.html
Code ∙ Version 6 
Finally, let's update the file extension handling to make sure we properly identify video files from Discord:


app.py
Code ∙ Version 9 
Let's rebuild the Docker container with these fixes:

The main issue was that Discord sends HTML snippets when you drag media, not the direct media URL
We need to extract the actual media URL from the HTML to download the file
We've improved file extension handling for videos
Here's what I recommend:

Stop your current container:
bash
docker-compose down
Rebuild the container with the new code:
bash
docker-compose build
Start the container again:
bash
docker-compose up -d
Check the logs to see if it's working:
bash
docker-compose logs -f
Try draggging media from Discord again and see if it works now
What Changed
HTML Parsing: Now we extract the actual media URL from the HTML snippet Discord sends when dragging
Look for the data-safe-src attribute which contains the direct media URL
Fall back to the href attribute if needed
Improved File Extension Detection:
Better handling of video files (mp4, webm)
Uses both content-type headers and URL patterns to determine the correct extension
Properly handles URLs without extensions
Better Error Handling:
More detailed logging
Checks for invalid URLs before attempting to download
Provides more helpful error messages
The app should now correctly download media files from Discord, including GIFs and videos, with the proper file extensions.




i changed the version of python to python:3.12-slim also in the dockerfile.

That's great to know you updated to Python 3.12. Let's continue troubleshooting your Discord Image Downloader.

The main problem we identified is that when you drag content from Discord, it's sending HTML instead of direct media URLs. The code I just provided should fix this by:

Extracting the actual media URL from the HTML (looking for data-safe-src attribute)
Properly handling video files and various file types
Applying the correct file extensions
Let's test this with one more improvement specific to Discord's media handling. Discord often uses URLs ending with .mp4 for GIFs as well, so we need to make sure we're correctly identifying the content type.


app.py
Code ∙ Version 10 
Let's also make one final improvement to extract URLs more effectively, as Discord's format can be quirky:


app.py
Code ∙ Version 11 
Let's add a special handler for Tenor URLs to extract the actual GIF directly:


tenor_handler.py
Code 
Now, let's update the app.py to use our Tenor handler:


app.py
Code ∙ Version 12 
Finally, let's update the app.py to use our Tenor handler when we encounter Tenor URLs:


app.py
Code ∙ Version 13 
Now let's rebuild the Docker container with these extensive fixes:

Stop the current container:
bash
docker-compose down
Rebuild with the new code:
bash
docker-compose build
Start it again:
bash
docker-compose up -d
What's Been Fixed
I've made significant improvements to fix the issues you were experiencing:

HTML Parsing: Discord sends HTML snippets when you drag content, not direct URLs
We now properly extract URLs from the HTML structure
We handle both data-safe-src and href attributes
Tenor GIF Handling: Added special handling for Tenor links
Created a dedicated Tenor handler that can extract direct GIF/MP4 URLs from Tenor pages
Uses multiple methods to find the media URL (JSON-LD, meta tags, regex)
Discord URL Handling: Discord often uses URLs ending with .mp4 for GIFs
Added Discord-specific logic to handle their URL patterns
Better detection of content types specific to Discord media
Improved File Extension Detection:
Better handling of video files (mp4, webm)
Properly applies file extensions based on both content type and URL patterns
The app should now correctly download media from Discord, including:

Regular images (PNG, JPG)
GIFs
Animated content that Discord serves as MP4
Tenor GIFs and videos
When you drag media from Discord now, the app will extract the actual media URL and download it directly, applying the proper file extension.





2025-04-20 14:31:44,670 - __main__ - INFO - Download directory set to: /app/downloads 2025-04-20 14:31:44,672 - __main__ - INFO - Starting Discord Image Downloader app... 2025-04-20 14:31:44,699 - werkzeug - INFO - [31m[1mWARNING: This is a development server. Do not use it in a production deploym

pasted

its working way better now but i noticed when it downloads animated things it downsload as mp4, thats fine but it also tries to save a file as a gif but its not got a .gif file extension plus adding that it the file doesnt cause it to work, so we need a check somewhere to not download files that have no file extensions

It looks like we've made a lot of progress! The app is now successfully downloading images and videos from Discord. I can see from your logs that it's properly extracting the direct media URLs and handling Discord's CDN links correctly.

Let's fix that remaining issue with animated content and proper file extensions. You're right that we need to add a check to ensure we don't download files without proper extensions or handle animated content better.


app.py
Code ∙ Version 14 

app.py
Code ∙ Version 15 

app.py
Code ∙ Version 16 
Now let's update the HTML file to make it clearer which URLs are supported:


templates/index.html
Code ∙ Version 7 
Let's update the filename extraction for better handling of Discord's CDN URLs:


app.py
Code ∙ Version 17 
Let's update the frontend JavaScript to better handle animated content:


templates/index.html
Code ∙ Version 8 
Let's rebuild the Docker container with these improvements:

Stop the current container:
bash
docker-compose down
Rebuild with the new code:
bash
docker-compose build
Start it again:
bash
docker-compose up -d
What's Been Fixed
I've made several improvements to fix the issues with file extensions and better handle animated content:

File Extension Validation:
Added a check to ensure all files have valid extensions
Improved detection and handling of file types based on content
Reject HTML content unless explicitly requested
Animated Content Handling:
Better detection of animated GIFs served as MP4s from Discord
Properly applies correct extensions based on content type
Warns when trying to download files without proper extensions
Discord-Specific URL Handling:
Skip Discord channel links (URLs that contain discord.com/channels/ but no file extension)
Improved extraction of direct media URLs from HTML content
Added support for src attribute in addition to data-safe-src
Better Filenames:
Uses Discord message IDs to create more meaningful filenames
Replaces generic "image0.jpg" filenames with more descriptive ones
Ensures all filenames have correct extensions
UI Improvements:
Added text clarifying supported file types
Better error messages when files can't be downloaded
These changes should resolve the issues you were experiencing with animated content and file extensions. The app now properly identifies the content type and ensures appropriate file extensions are used. It also skips Discord channel links and other non-media URLs, focusing only on downloading actual media files.




will you update the readme and include all changes and additions since the beginning of the project and proper version changes changelog ect, make it professional and pretty please

I'll create a comprehensive and professional README with all the changes and additions we've made since the beginning of the project, including a proper changelog.


README.md
Document ∙ Version 4 
I've created a comprehensive, professional README document that details all aspects of your Discord Image Downloader project. Here's what I've included:

README Contents
Project Overview: A concise explanation of what the app does with feature badges for quick reference
Features List: Detailed breakdown of all capabilities we've implemented
Quick Start Guide: Simple instructions for getting up and running with Docker
Usage Instructions: Step-by-step guide for end users
Technical Details: Information about the architecture and file structure
Troubleshooting Section: Debug pages, common issues, and how to resolve them
Alternative Deployment Options: Information about using Uvicorn instead of Flask
Detailed Changelog:
v1.0.0: Initial release with all features
v0.3.0: Log improvements, filename handling and animated content fixes
v0.2.0: Debug page, HTML extraction, console logging
v0.1.0: Initial implementation with basic functionality
Planned Features: Ideas for future development
License & Acknowledgements: Credits to the technologies used
The README is formatted with proper Markdown styling, badges, and structure to look professional and organized. It provides both technical details for developers and clear instructions for end users.

Would you like me to make any specific additions or changes to this README? Perhaps add more technical details or expand any particular section?




can we make the debug page live ? refresh wise. as in updating auto when any action is happening, also i would like the index.html and debug.html to be a much dark theme color wise, also possibly add a thin and fixed header and a thin footer to both, modern and sleek please with a couple test links in the header and some git image links in the footer with copyright and name

I'd be happy to make those enhancements to create a more modern, dark-themed interface with auto-refreshing capabilities for the debug page. Let's start by updating the debug page to auto-refresh with a live view, and then implement a dark theme with header and footer across both pages.


templates/debug.html
Code ∙ Version 2 

Making edits...
Code ∙ Version 9 




Continue

Let me finish creating the updated index.html file with the new dark theme, header, and footer:


templates/index.html
Code ∙ Version 10 
Now let's also update the logs page to match our new dark theme and include the header and footer:


Making edits...
Code ∙ Version 2 




continue

Let me finish creating the logs page:


templates/logs.html
Code 
Let's update the app.py file to include our new templates:


app.py
Code 
Summary of Updates
I've completely redesigned the user interface with a modern dark theme and added several important enhancements:

1. Dark Theme Interface
Applied a sleek dark color scheme across all pages
Created a consistent header and footer for better navigation
Added modern styling with smooth transitions and hover effects
2. Auto-Refreshing Debug Page
Implemented automatic refreshing with a 5-second interval
Added visual indicators for refresh status
Created a modern grid layout for downloaded files
3. Enhanced Logs Page
Added real-time log refreshing
Implemented log filtering by level (INFO, WARNING, ERROR)
Added search functionality to find specific log entries
Included color-coding for different log levels
4. Improved Main Interface
Clearer drop area with better visual feedback during drag
Improved error notifications that stay visible longer
Added responsive design that works on various screen sizes
5. Navigation Improvements
Consistent navigation bar across all pages
Visual indicators for the current page
Quick access to debug and logs pages
Implementation Details
The auto-refres




from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import requests
from urllib.parse import urlparse
import uuid
import logging
import io
import datetime
from threading import Lock

# Configure logging
log_stream = io.StringIO()
file_handler = logging.FileHandler('downloads/app.log')
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

# Create download directory if it doesn't exist
DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
logger.info(f"Download directory set to: {DOWNLOAD_DIR}")

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
            import re
            safe_src_match = re.search(r'data-safe-src=["\']([^"\']+)["\']', image_url)
            
            if safe_src_match:
                # Found the direct media URL
                extracted_url = safe_src_match.group(1)
                logger.info(f"Extracted URL from HTML: {extracted_url}")
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
                            # First, check if there's already a direct URL in the HTML
                            media_match = re.search(r'https://media\.tenor\.com/[^"\']+\.(gif|mp4|webm)', image_url)
                            if media_match:
                                media_url = media_match.group(0)
                                logger.info(f"Found direct Tenor media URL in HTML: {media_url}")
                                image_url = media_url
                            else:
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
                        # Really default case
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
                    filename = f"{filename.split('.')[0]}.jpg"
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
                'message': f'Image downloaded successfully as {filename}'
            })
        else:
            logger.error(f"File was not saved at {file_path}")
            return jsonify({'success': False, 'message': 'File was not saved'})
        
    except Exception as e:
        logger.exception(f"Error downloading image: {str(e)}")
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)

@app.route('/debug')
def debug_info():
    """A simple debug page to help with troubleshooting"""
    debug_info = {
        'download_dir': DOWNLOAD_DIR,
        'download_dir_exists': os.path.exists(DOWNLOAD_DIR),
        'download_dir_writable': os.access(DOWNLOAD_DIR, os.W_OK),
        'files_in_download_dir': sorted(os.listdir(DOWNLOAD_DIR)) if os.path.exists(DOWNLOAD_DIR) else [],
        'app_directory': os.path.dirname(os.path.abspath(__file__)),
        'environment': dict(os.environ)
    }
    
    return render_template('debug.html', debug_info=debug_info)

@app.route('/logs')
def view_logs():
    """View application logs in the browser"""
    # Get logs from the StringIO buffer
    log_content = log_stream.getvalue()
    
    # Read from log file if the buffer is empty
    if not log_content and os.path.exists('downloads/app.log'):
        try:
            with open('downloads/app.log', 'r') as f:
                log_content = f.read()
        except Exception as e:
            log_content = f"Error reading log file: {str(e)}"
    
    return render_template('logs.html', logs=log_content)

if __name__ == '__main__':
    logger.info("Starting Discord Image Downloader app...")
    app.run(host='0.0.0.0', port=5000, debug=True)
