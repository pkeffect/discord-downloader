# Discord Image and GIF Downloader
![image](https://github.com/user-attachments/assets/eaed13c4-02ef-4196-abc7-ab657f113df7)


This project is a web application that allows users to easily download images and GIFs from Discord by dragging and dropping them into the browser. It uses Flask for the backend and vanilla JavaScript with Tailwind CSS for the frontend.

## Features

- Drag and drop interface for Discord images and GIFs
- Supports both image and GIF downloads
- Real-time feedback with success/error messages
- Responsive design using Tailwind CSS

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

## Setup and Installation

1. Clone the repository or download the source code:   ```
   git clone https://github.com/yourusername/discord-image-downloader.git
   cd discord-image-downloader   ```

2. Create a virtual environment (optional but recommended):   ```
   python -m venv venv   ```

3. Activate the virtual environment:
   - On Windows:     ```
     venv\Scripts\activate     ```
   - On macOS and Linux:     ```
     source venv/bin/activate     ```

4. Install the required packages:   ```
   pip install flask requests   ```





## Running the Application

1. Navigate to the `imgdownloader` directory:
   ```
   cd imgdownloader
   ```

2. Run the Flask application:
   ```
   python app.py
   ```

3. Open a web browser and go to `http://127.0.0.1:5000/`

4. You should now see the Discord Image Downloader interface. You can drag and drop Discord image or GIF links into the designated area to download them.

## How It Works

### Backend (app.py)

The `app.py` file contains the Flask application that handles the server-side logic:

- It sets up a route for the main page (`/`) that renders the `index.html` template.
- It provides an endpoint (`/download_image`) that receives POST requests with image URLs.
- When a valid Discord image or GIF URL is received, it downloads the file and saves it to the `static/downloads` directory.
- It determines the correct file extension based on the content type of the downloaded file.
- It returns JSON responses indicating the success or failure of the download operation.

### Frontend (index.html)

The `index.html` file contains the HTML structure, Tailwind CSS styling, and JavaScript for the user interface:

- It provides a drag-and-drop area for users to drop Discord image or GIF links.
- It uses JavaScript to handle the drag-and-drop events and send AJAX requests to the backend.
- It displays success or error messages using a floating alert at the top of the page.
- The design is responsive and uses Tailwind CSS for styling.

## Customization

- To change the download directory, modify the `DOWNLOAD_FOLDER` variable in `app.py`.
- To adjust the styling, you can modify the Tailwind classes in `index.html` or extend the Tailwind configuration.

## Troubleshooting

- If you encounter any "Permission denied" errors when saving files, ensure that the application has write permissions for the `static/downloads` directory.
- If the downloads folder is not created automatically, create it manually in the `static` directory.
- Make sure you're using a modern web browser that supports the Drag and Drop API.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

- Flask: https://flask.palletsprojects.com/
- Tailwind CSS: https://tailwindcss.com/
- Requests: https://docs.python-requests.org/

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
