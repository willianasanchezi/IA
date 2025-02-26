import requests
import json
import sqlite3

def preguntar_al_modelo(pregunta):
    """
    Envía una pregunta al modelo de Ollama, muestra la respuesta en tiempo real
    y guarda la pregunta y respuesta en SQLite.
    """
    # Conectar a la base de datos (se crea si no existe)
    conn = sqlite3.connect('preguntas_respuestas.db')
    cursor = conn.cursor()

    # Crear la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preguntas_respuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT,
            respuesta TEXT
        )
    ''')
    conn.commit()

    # URL del API de Ollama
    url = "http://localhost:11434/api/generate"
    
    # Payload con el modelo y la pregunta
    payload = {
        "model": "deepseek-r1:14b",  # Modelo a usar
        "prompt": f"responder en español. Razona en español sin traducir el razonamiento a inglés. {pregunta}",  # Pregunta ingresada por el usuario
        "stream": True  # Habilitar streaming
    }

    respuesta_completa = ""

    # Enviar la solicitud al API
    with requests.post(url, json=payload, stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    # Convertir cada fragmento a JSON y mostrar la respuesta
                    chunk = json.loads(line.decode("utf-8"))
                    respuesta_completa += chunk["response"]
                    yield chunk["response"]  # Enviar la respuesta en tiempo real
        else:
            yield f"Error: {response.status_code} {response.text}"

    # Guardar la pregunta y respuesta en la base de datos
    cursor.execute('''
        INSERT INTO preguntas_respuestas (pregunta, respuesta)
        VALUES (?, ?)
    ''', (pregunta, respuesta_completa))
    conn.commit()

    # Cerrar la conexión
    conn.close()
