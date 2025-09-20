import os
import random

from flask import Flask, jsonify, request, send_from_directory
from quantum_engine import execute_quantum_command, simulate_neural_response

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/create_plane', methods=['POST'])
def create_plane():
    data = request.json
    plane_name = data.get('plane_name', 'Default Plane')
    plane_type = data.get('plane_type', 'Default Type')
    neural_response = simulate_neural_response(plane_name, plane_type)
    return jsonify(neural_response)

@app.route('/execute_command', methods=['POST'])
def execute_command():
    data = request.json
    command = data.get('command', '')
    output = execute_quantum_command(command)
    return jsonify(output)

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
