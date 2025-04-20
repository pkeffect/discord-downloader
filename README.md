# Discord Media Download

![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)
![Docker](https://img.shields.io/badge/docker-compatible-green.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)

A lightweight, containerized web application that allows you to easily download images, GIFs, and videos from Discord by simply dragging and dropping them into your browser.

<p align="center">
  <img src="https://github.com/yourusername/discord-media-download/raw/main/screenshots/main-interface.png" alt="Main Interface" width="600">
  <br>
  <em>Modern, dark-themed interface with easy drag & drop functionality</em>
</p>

## Features

- **Easy-to-Use Interface**: Simple drag-and-drop functionality with dark theme design
- **Multiple Format Support**: Downloads images, GIFs, animated GIFs (as MP4), videos, and WebP files
- **Intelligent URL Extraction**: Automatically extracts media URLs from Discord's HTML snippets
- **Proper File Extensions**: Ensures all files have the correct extension based on content type
- **Duplicate File Handling**: Automatically adds sequential numbering (001, 002, etc.) to duplicate filenames
- **Tenor GIF Support**: Special handling for Tenor GIFs shared through Discord
- **Live Monitoring**: Real-time log viewing and auto-refreshing debug interface
- **Advanced Filtering**: Search and filter logs by level (INFO, WARNING, ERROR)
- **Containerized Deployment**: Easy setup with Docker
- **Modular Architecture**: Well-organized codebase with proper separation of concerns
- **Templating System**: Consistent UI across all pages using Flask's template inheritance
- **Thumbnail Previews**: Visual thumbnails for images in the debug file listing
- **Pagination**: Organized file viewing with pagination for large collections
- **Granular Logging**: Separate log files for different components and log levels
- **Configuration System**: JSON-based configuration for easy customization

## Screenshots

<p align="center">
  <img src="https://github.com/yourusername/discord-media-download/raw/main/screenshots/debug-interface.png" alt="Debug Interface" width="600">
  <br>
  <em>Auto-refreshing debug interface with file monitoring and thumbnails</em>
</p>

<p align="center">
  <img src="https://github.com/yourusername/discord-media-download/raw/main/screenshots/logs-interface.png" alt="Logs Interface" width="600">
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
   git clone https://github.com/yourusername/discord-media-download.git
   cd discord-media-download
   ```

2. The necessary directories will be created automatically by the application. Start the container:
   ```bash
   docker-compose up -d
   ```

3. Access the application in your browser:
   ```
   http://localhost:5000
   ```

## Usage

1. Open Discord in your browser or desktop app
2. Find an image, GIF, or video you want to download
3. Drag the media directly into the drop area in the Discord Media Download web app
4. The file will be downloaded to the `downloads` folder with the appropriate file extension
5. If a file with the same name already exists, a sequential number will be added (e.g., image_001.jpg)

## Technical Details

### Architecture

The application consists of:

- **Flask Backend**: Modular design using blueprints for better organization
- **Tailwind CSS**: For responsive and modern UI
- **Docker**: For containerization and easy deployment
- **JavaScript**: For real-time updates and UI interactions
- **Jinja2 Templates**: For consistent UI with template inheritance
- **JSON Configuration**: For flexible application settings

The application follows a clean, modular architecture with separation of concerns:

- **Routes**: Handle HTTP requests and responses
- **Services**: Contain business logic for downloading and processing media
- **Utils**: Provide utility functions like logging
- **Templates**: Use base layout with template inheritance for consistent UI
- **Config**: Central JSON-based configuration for easy customization

### File Structure

```
discord_media_download/
│
├── app.py                   # Main Flask application
├── config.py                # Centralized configuration
├── config.json              # User-editable configuration settings
│
├── routes/                  # Route handlers organized by feature
│   ├── __init__.py
│   ├── main_routes.py       # Home page routes
│   ├── download_routes.py   # Download functionality
│   └── debug_routes.py      # Debug and logs routes
│
├── services/                # Business logic layer
│   ├── __init__.py
│   ├── download_service.py  # Media download logic
│   ├── file_service.py      # File handling functionality
│   └── tenor_service.py     # Handler for Tenor GIFs
│
├── utils/                   # Utility functions
│   ├── __init__.py
│   └── logging_utils.py     # Logging configuration
│
├── static/                  # Static files directory
│   ├── css/
│   │   └── styles.css       # Common styles
│   │
│   ├── favicon.ico          # Application favicon
│   │
│   └── js/
│       ├── tailwind-config.js  # Tailwind configuration
│       ├── main.js             # Shared JavaScript functions
│       ├── index.js            # Home page scripts
│       ├── debug.js            # Debug page scripts
│       └── logs.js             # Logs page scripts
│
├── templates/               # HTML templates
│   ├── layout.html          # Base template with header and footer
│   ├── index.html           # Home page template
│   ├── debug.html           # Debug page template
│   ├── logs.html            # Logs page template
│   ├── header.html          # Header component
│   └── footer.html          # Footer component
│
├── downloads/               # Directory for downloaded files
│
└── logs/                    # Application logs directory
    ├── app.log              # Main application log
    ├── downloads.log        # Download-specific logs
    ├── errors.log           # Error-only logs
    └── debug.log            # Debug-level logs
```

## Advanced Features

### Auto-Refreshing Debug Page

The debug page automatically refreshes every 5 seconds to show:

- System information (OS, Python version, memory usage)
- Live list of downloaded files with thumbnails
- Environment variables
- Container status
- Pagination for large file collections

You can toggle auto-refresh, manually refresh, or view file details directly from this interface.

### Live Log Viewer

The logs page provides real-time monitoring capabilities:

- Color-coded log levels for better readability
- Filtering by log level (INFO, WARNING, ERROR)
- Full-text search functionality
- Auto-scroll to latest entries
- Manual and automatic refresh options
- Proper line wrapping for long log entries

### Template Inheritance

The application uses Flask's Jinja2 template inheritance for consistent UI across all pages:

- Base layout template (`layout.html`) defines the overall page structure
- Page-specific templates extend the base layout and inject content
- Header and footer components are included consistently across all pages
- Each page can add its own custom scripts and styles when needed

### Configuration System

The application uses a flexible JSON-based configuration system:

- User-editable `config.json` file for customizing application settings
- Default configuration provided if no config file exists
- Separate logging configuration for different components
- Easily extensible for new features and settings

## Troubleshooting

### Debug and Logs Pages

The application includes two helpful pages for debugging:

- **Debug Page**: Shows system information, downloaded files with thumbnails, and environment variables
  - Access at: `http://localhost:5000/debug`
  - Provides pagination for large file collections

- **Logs Page**: Shows detailed application logs right in your browser
  - Access at: `http://localhost:5000/logs`
  - Logs are color-coded by level (INFO, DEBUG, WARNING, ERROR)
  - Properly wraps long log lines for better readability

### Common Issues

1. **Media not downloading**:
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
   docker exec -it discord_downloader python test_download.py https://example.com/image.jpg
   ```

4. **Manual volume permission fix**:
   ```bash
   docker exec -it discord_downloader chmod -R 777 /app/downloads
   ```

## Alternative Deployment Options

### Using Uvicorn (ASGI)

If you prefer using Uvicorn instead of the default Flask server:

1. Add `uvicorn` to requirements.txt:
```
flask==2.3.3
requests==2.31.0
uvicorn==0.23.2
psutil==5.9.5
Pillow==10.0.0
```

2. Modify the Dockerfile CMD:
```dockerfile
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
```

## Changelog

### v1.4.0 (2025-04-20)
- Added duplicate file detection with automatic sequential numbering
- Fixed log display overflow with proper line wrapping
- Created separate log files for different components and log levels
- Added thumbnail previews for files in the debug interface
- Implemented pagination for file listings
- Added favicon
- Created JSON-based configuration system
- Enhanced footer with license and version info
- Added current date and time display
- Improved error notification persistence
- Implemented template inheritance with a base layout template
- Fixed header and footer display issues across all pages
- Added proper CSS file reference consistency
- Updated template inclusion mechanism in app.py
- Enhanced UI consistency across the application
- Improved the context processor for template handling

### v1.3.0 (2025-04-20)
- Completely refactored codebase to modular architecture
- Implemented Flask blueprints for better route organization
- Separated core functionality into service layers
- Centralized configuration in config.py
- Improved logging with dedicated utilities
- Enhanced error handling throughout the application
- Updated documentation with current architecture

### v1.2.0 (2025-04-20)
- Refactored to modular architecture
- Separated HTML components (header, footer)
- Organized JavaScript and CSS into separate files
- Rebranded from "Discord Image Downloader" to "Discord Media Download"
- Improved file structure for better maintainability
- Enhanced media extraction from multiple sources
- Optimized server-side file handling

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

## Planned Features

- [ ] Multiple file download support
- [ ] Custom download location setting
- [ ] Discord webhook integration
- [ ] Image preview before download
- [ ] Video/GIF thumbnail generation
- [ ] Auto-categorization of downloaded files
- [ ] User-defined naming patterns
- [ ] Background download queue
- [ ] Improved mobile support

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine for Python
- [Tailwind CSS](https://tailwindcss.com/) - For the UI
- [Docker](https://www.docker.com/) - For containerization
- [Python Requests](https://requests.readthedocs.io/) - For HTTP handling
- [Discord Image and GIF Downloader](https://github.com/ztxv/discord-image-downloader) - For original project, thanks!