# Discord Image Downloader

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Docker](https://img.shields.io/badge/docker-compatible-green.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)

A lightweight, containerized web application that allows you to easily download images, GIFs, and videos from Discord by simply dragging and dropping them into your browser.

<p align="center">
  <img src="https://github.com/yourusername/discord-image-downloader/raw/main/screenshots/main-interface.png" alt="Main Interface" width="600">
  <br>
  <em>Modern, dark-themed interface with easy drag & drop functionality</em>
</p>

## Features

- **Easy-to-Use Interface**: Simple drag-and-drop functionality with dark theme design
- **Multiple Format Support**: Downloads images, GIFs, animated GIFs (as MP4), videos, and WebP files
- **Intelligent URL Extraction**: Automatically extracts media URLs from Discord's HTML snippets
- **Proper File Extensions**: Ensures all files have the correct extension based on content type
- **Tenor GIF Support**: Special handling for Tenor GIFs shared through Discord
- **Live Monitoring**: Real-time log viewing and auto-refreshing debug interface
- **Advanced Filtering**: Search and filter logs by level (INFO, WARNING, ERROR)
- **Containerized Deployment**: Easy setup with Docker

## Screenshots

<p align="center">
  <img src="https://github.com/yourusername/discord-image-downloader/raw/main/screenshots/debug-interface.png" alt="Debug Interface" width="600">
  <br>
  <em>Auto-refreshing debug interface with file monitoring</em>
</p>

<p align="center">
  <img src="https://github.com/yourusername/discord-image-downloader/raw/main/screenshots/logs-interface.png" alt="Logs Interface" width="600">
  <br>
  <em>Advanced log viewer with filtering and search capabilities</em>
</p>

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/discord-image-downloader.git
   cd discord-image-downloader
   ```

2. Create the downloads folder with proper permissions:
   ```bash
   mkdir -p downloads
   chmod 777 downloads
   ```

3. Start the container:
   ```bash
   docker-compose up -d
   ```

4. Access the application in your browser:
   ```
   http://localhost:5000
   ```

## Usage

1. Open Discord in your browser or desktop app
2. Find an image, GIF, or video you want to download
3. Drag the media directly into the drop area in the Discord Image Downloader web app
4. The file will be downloaded to the `downloads` folder with the appropriate file extension

## Technical Details

### Architecture

The application consists of:

- **Flask Backend**: Serves the web interface and handles download requests
- **Tailwind CSS**: For responsive and modern UI
- **Docker**: For containerization and easy deployment
- **JavaScript**: For real-time updates and UI interactions

### File Structure

```
.
├── app.py                 # Flask application
├── tenor_handler.py       # Special handler for Tenor URLs
├── templates
│   ├── index.html         # Main HTML page
│   ├── debug.html         # Debug information page
│   └── logs.html          # Log viewer page
├── downloads              # Where downloaded files are saved
├── logs                   # Application logs
├── test_download.py       # Utility to test downloads
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
└── docker-compose.yml     # Docker Compose configuration
```

## Advanced Features

### Auto-Refreshing Debug Page

The debug page automatically refreshes every 5 seconds to show:

- System information
- Live list of downloaded files
- Environment variables
- Container status

You can toggle auto-refresh, manually refresh, or view file details directly from this interface.

### Live Log Viewer

The logs page provides real-time monitoring capabilities:

- Color-coded log levels for better readability
- Filtering by log level (INFO, WARNING, ERROR)
- Full-text search functionality
- Auto-scroll to latest entries
- Manual and automatic refresh options

## Troubleshooting

### Debug and Logs Pages

The application includes two helpful pages for debugging:

- **Debug Page**: Shows system information, downloaded files, and environment variables
  - Access at: `http://localhost:5000/debug`

- **Logs Page**: Shows detailed application logs right in your browser
  - Access at: `http://localhost:5000/logs`
  - Logs are color-coded by level (INFO, DEBUG, WARNING, ERROR)

### Common Issues

1. **Images not downloading**:
   - Check if the downloads directory has proper permissions
   - Ensure the container has write access to the volume
   - Look at the logs for detailed errors

2. **Viewing logs**:
   ```bash
   docker-compose logs -f discord_downloader
   ```

3. **Testing downloads directly**:
   ```bash
   # From inside the container
   docker exec -it discord_image_downloader python test_download.py https://example.com/image.jpg
   ```

4. **Manual volume permission fix**:
   ```bash
   docker exec -it discord_image_downloader chmod -R 777 /app/downloads
   ```

## Alternative Deployment Options

### Using Uvicorn (ASGI)

If you prefer using Uvicorn instead of the default Flask server:

1. Add `uvicorn` to requirements.txt:
```
flask==2.3.3
requests==2.31.0
uvicorn==0.23.2
```

2. Modify the Dockerfile CMD:
```dockerfile
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
```

## Changelog

### v1.1.0 (2025-04-20)
- Added modern dark theme interface
- Implemented auto-refreshing debug page
- Created advanced log viewer with filtering and search
- Added consistent navigation header and footer
- Improved error notifications with longer display time
- Enhanced visual feedback during drag and drop
- Added responsive design for various screen sizes

### v1.0.0 (2025-04-20)
- Initial public release
- Dockerized deployment
- Support for images, GIFs, and videos
- Automatic file extension detection
- Tenor GIF special handling

### v0.3.0 (2025-04-20)
- Added better logs page with color-coded log levels
- Improved filename generation for Discord URLs
- Fixed handling of animated content
- Added validation for file extensions
- Added channel link detection and filtering

### v0.2.0 (2025-04-20)
- Added debug page with system information
- Added HTML content extraction for Discord media
- Fixed syntax errors and implementation bugs
- Added browser console logging
- Added in-app logs page
- Improved error handling for network requests

### v0.1.0 (2025-04-20)
- Initial implementation
- Basic drag and drop functionality
- Simple Flask backend
- Docker container setup
- Basic error handling

## Planned Features

- [ ] Multiple file download support
- [ ] Custom download location setting
- [ ] Discord webhook integration
- [ ] Image preview before download
- [ ] Video/GIF thumbnail generation
- [ ] Auto-categorization of downloaded files

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Tailwind CSS](https://tailwindcss.com/) - For the UI
- [Docker](https://www.docker.com/) - For containerization
- [Python Requests](https://requests.readthedocs.io/) - For HTTP handling