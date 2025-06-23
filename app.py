from flask import Flask, request, jsonify
import io
import contextlib
import requests
import os

app = Flask(__name__)

@app.route('/')
def inicio():
    return "Servidor activo para Python y SageMath."

# Ejecuta código Python localmente
@app.route('/ejecutar', methods=['POST'])
def ejecutar_python():
    data = request.get_json()
    codigo = data.get('codigo', '')
    buffer = io.StringIO()

    try:
        with contextlib.redirect_stdout(buffer):
            exec(codigo, {})
        return jsonify({'resultado': buffer.getvalue()})
    except Exception as e:
        return jsonify({'resultado': f'Error: {str(e)}'})

# Envía código a SageMathCell
@app.route('/sagemath', methods=['POST'])
def ejecutar_sagemath():
    data = request.get_json()
    codigo = data.get('codigo', '')

    try:
        response = requests.post(
            'https://sagecell.sagemath.org/service',
            json={"code": codigo},
            timeout=20
        )
        if response.status_code == 200:
            resultado = response.json().get("stdout", "Sin salida")
            return jsonify({'resultado': resultado})
        else:
            return jsonify({'resultado': f'Error HTTP: {response.status_code}'})
    except Exception as e:
        return jsonify({'resultado': f'Error: {str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
