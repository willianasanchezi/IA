from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt  # Not directly used in web display, but needed for DeepFace

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Add more if needed
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Create the directory if it doesn't exist

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                # Analyze the image
                demography = DeepFace.analyze(filepath)
                # Extract relevant information for display (avoid plotting in web)
                dominant_emotion = demography[0]['dominant_emotion']
                age = demography[0]['age']
                gender = demography[0]['gender']
                race = demography[0]['dominant_race']


                return render_template('result.html', filename=filename, dominant_emotion=dominant_emotion, age=age, gender=gender, race = race)

            except Exception as e:  # Handle potential DeepFace errors
                error_message = str(e)
                return render_template('error.html', error_message=error_message, filename = filename)

    return render_template('index.html')


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename)) # Serve image from static folder



if __name__ == '__main__':
    app.run(debug=True)
