from flask import Flask, request, jsonify
import io
import contextlib
import requests
import os

app = Flask(__name__)

@app.route('/')
def inicio():
    return "Servidor de ejecución Python y SageMath activo."

# Endpoint para ejecutar código Python
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

# Endpoint para ejecutar código SageMath
@app.route('/sagemath', methods=['POST'])
def ejecutar_sage():
    data = request.get_json()
    codigo = data.get('codigo', '')

    try:
        payload = {
            "code": codigo,
            "opts": {"output": "text"}
        }
        response = requests.post(
            "https://sagecell.sagemath.org/service",
            json=payload,
            timeout=10
        )
        
        try:
            respuesta_json = response.json()
        except ValueError:
            return jsonify({
                "success": False,
                "stdout": "Error al contactar SageMathCell: Respuesta no válida",
                "raw": response.text
            })

        return jsonify({
            "success": True,
            "stdout": respuesta_json.get("stdout", ""),
            "stderr": respuesta_json.get("stderr", ""),
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "stdout": f"Error al contactar SageMathCell: {str(e)}"
        })
