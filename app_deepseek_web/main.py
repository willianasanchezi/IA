from flask import Flask, render_template, request, Response, stream_with_context
from ollama_module_db import preguntar_al_modelo

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pregunta_usuario = request.form['pregunta']
        return Response(stream_with_context(preguntar_al_modelo(pregunta_usuario)), content_type='text/plain')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='192.168.0.60')
