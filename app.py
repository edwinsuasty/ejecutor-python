from flask import Flask, request, jsonify
import io
import contextlib

app = Flask(__name__)

@app.route('/')
def inicio():
    return "Servidor de ejecución Python activo."

@app.route('/ejecutar', methods=['POST'])
def ejecutar():
    data = request.get_json()
    codigo = data.get('codigo', '')
    buffer = io.StringIO()

    try:
        with contextlib.redirect_stdout(buffer):
            exec(codigo, {})
        return jsonify({'resultado': buffer.getvalue()})
    except Exception as e:
        return jsonify({'resultado': f'Error: {str(e)}'})
