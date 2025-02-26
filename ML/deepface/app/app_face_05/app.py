from flask import Flask, render_template, request, redirect, url_for
import os
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt

app = Flask(__name__)

# Configuración de la carpeta de subida de imágenes
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verificar si se ha cargado un archivo
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # Si no se selecciona ningún archivo, redirigir al inicio
        if file.filename == '':
            return redirect(request.url)
        
        # Guardar el archivo en la carpeta de subidas
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Procesar la imagen con DeepFace
        try:
            img = cv2.imread(file_path)
            demography = DeepFace.analyze(file_path)
            
            # Mostrar la imagen usando matplotlib (opcional)
            plt.imshow(img[:, :, ::-1])
            plt.title("Imagen Cargada")
            plt.show()
            
            # Retornar los resultados al usuario
            return render_template('index.html', result=demography)
        except Exception as e:
            return render_template('index.html', error=str(e))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
