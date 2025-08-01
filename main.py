from flask import Flask, request, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
from collections import Counter
from time import time


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check valid file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_top_colors(image_path, top_n=10):
    img = Image.open(image_path)
    img.thumbnail((200, 200))
    img = img.convert('RGB')
    data = np.array(img)
    pixels = data.reshape((-1, 3))

    counts = Counter(map(tuple, pixels))
    total_pixels = len(pixels)
    top_colors = counts.most_common(top_n)
    
    color_data = []
    for color, count in top_colors:
        percentage = f"{round((count / total_pixels) * 100, 3)}%"
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        color_data.append((hex_color, percentage))
        
    return color_data


@app.route("/", methods=['GET', 'POST'])
def home():

    default_image = "static/img/image.jpg"
    color_data = extract_top_colors(default_image)


    filename = None
    if request.method == 'POST':
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = "uploaded_image.jpg"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            color_data = extract_top_colors(file_path)
    return render_template("index.html",colors=color_data, filename=filename, time=time)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)

    