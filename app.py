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
    codigo = data.get('code', '')

    try:
        response = requests.post(
            "https://sagecell.sagemath.org/service",
            json={"code": codigo},
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=10
        )
        result = response.json()
        return jsonify({
            "success": True,
            "stdout": result.get("stdout", "")
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "stdout": f"Error al contactar SageMathCell: {str(e)}"
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
