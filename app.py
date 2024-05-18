from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO
import cv2

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load YOLOv8 model
model = YOLO('PPE.pt')  # Adjust to the specific YOLOv8 model you are using

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Run YOLOv8 inference
        results = model(filepath)
        
        # Save the result image with annotations
        result_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_' + filename)
        for result in results:
            annotated_frame = result.plot()  # Get annotated image
            cv2.imwrite(result_image_path, annotated_frame)

        return redirect(url_for('uploaded_file', filename='result_' + filename))
    return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('uploaded_file.html', filename=filename)

@app.route('/static/uploads/<filename>')
def send_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    result_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    original_file_path = result_file_path.replace('result_', '')

    try:
        if os.path.exists(result_file_path):
            os.remove(result_file_path)
        if os.path.exists(original_file_path):
            os.remove(original_file_path)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
