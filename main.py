from flask import Flask, request, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check valid file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def home():
    color_data = {
        "#481830": 0.301746,
        "#783030": 0.212460,
        "#306078": 0.166667,
        "#486090": 0.084683,
        "#183060": 0.082381,
        "#d86048": 0.053175,
        "#a84830": 0.037222,
        "#300018": 0.026349,
        "#781818": 0.017857,
        "#f0d860": 0.007857
    }
    filename = None
    if request.method == 'POST':
        file = request.files.get('image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
    print(filename)
    return render_template("index.html",colors=color_data, filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)

    