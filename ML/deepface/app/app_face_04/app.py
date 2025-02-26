from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt

app = Flask(__name__)

# Configuramos la ruta para almacenar las imágenes subidas
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verificamos si el POST contiene un archivo
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            # Guardamos el archivo de manera segura
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Ejecutamos el análisis de DeepFace
            demography = DeepFace.analyze(filepath)

            # Cargamos la imagen con OpenCV y la mostramos usando Matplotlib
            img = cv2.imread(filepath)
            plt.imshow(img[:, :, ::-1])
            plt.show()

            # Renderizamos los resultados
            return render_template('index.html', demography=demography, uploaded_image=url_for('static', filename=f'uploads/{filename}'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
