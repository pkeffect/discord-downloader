from flask import Flask, render_template, request, jsonify
import os
import requests
import mimetypes

app = Flask(__name__)

# Specify the folder to save images and GIFs
DOWNLOAD_FOLDER = 'static/downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_image', methods=['POST'])
def download_image():
    image_url = request.form.get('image_url')
    if image_url:
        try:
            # Download the image or GIF
            response = requests.get(image_url)
            response.raise_for_status()

            # Determine the file extension based on content type
            content_type = response.headers.get('content-type')
            extension = mimetypes.guess_extension(content_type)

            if extension is None:
                # Fallback to .jpg if we can't determine the extension
                extension = '.jpg'

            # Extract the base filename without extension
            base_filename = os.path.basename(image_url.split("?")[0])
            base_filename = os.path.splitext(base_filename)[0]

            # Create the full filename with the correct extension
            filename = f"{base_filename}{extension}"

            # Save the image or GIF to the specified folder
            file_path = os.path.join(DOWNLOAD_FOLDER, filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)

            return jsonify({"success": True, "message": f"{filename} downloaded successfully!"})
        except Exception as e:
            return jsonify({"success": False, "message": f"Error downloading file: {e}"})
    else:
        return jsonify({"success": False, "message": "No image URL provided."})

if __name__ == '__main__':
    app.run(debug=True)
