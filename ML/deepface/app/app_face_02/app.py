from flask import Flask, render_template, request, redirect, url_for
import os
from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt

app = Flask(__name__)

# Configuración para la carpeta de subida de archivos
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verificar si se ha subido un archivo
        if 'file' not in request.files:
            return render_template('index.html', error="No se ha seleccionado ningún archivo.")
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('index.html', error="No se ha seleccionado ningún archivo.")
        
        if file:
            # Guardar la imagen en la carpeta de subida
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            try:
                # Analizar la imagen con DeepFace
                results = DeepFace.analyze(filepath, actions=['age', 'gender', 'emotion', 'race'])
                
                # Mostrar la imagen
                img = cv2.imread(filepath)
                plt.imshow(img[:, :, ::-1])
                plt.axis('off')
                output_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.png')
                plt.savefig(output_image_path)
                plt.close()
                
                # Redirigir a la página de resultados con los datos necesarios
                return redirect(url_for('results', image_url=file.filename))
            
            except Exception as e:
                return render_template('index.html', error=f"Error al analizar la imagen: {str(e)}")
    
    return render_template('index.html')

@app.route('/results')
def results():
    # Obtener la URL de la imagen desde los parámetros de la URL
    image_url = request.args.get('image_url')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_url)
    
    # Analizar la imagen con DeepFace
    results = DeepFace.analyze(filepath, actions=['age', 'gender', 'emotion', 'race'])
    
    # Pasar los resultados a la plantilla de resultados
    return render_template('result.html', results=results, image_url=image_url, output_image='output.png')

if __name__ == '__main__':
    app.run(debug=True)
