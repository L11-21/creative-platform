import random
from flask import Flask, jsonify, request, send_from_directory
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import os

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/create_plane', methods=['POST'])
def create_plane():
    data = request.json
    plane_name = data.get('plane_name', 'Default Plane')
    plane_type = data.get('plane_type', 'Default Type')
    neural_response = simulate_neural_network_with_qiskit(plane_name, plane_type)
    return jsonify(neural_response)

@app.route('/execute_command', methods=['POST'])
def execute_command():
    data = request.json
    command = data.get('command', '')
    # For demo: just run a basic circuit and echo the command
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    backend = AerSimulator()
    transpiled_qc = transpile(qc, backend)
    job = backend.run(transpiled_qc, shots=1)
    result = job.result().get_counts()
    key = list(result.keys())[0] if result else "00"
    output = {
        "output": f"Quantum output for '{command}': {key}"
    }
    return jsonify(output)

@app.route('/health')
def health():
    return 'OK', 200

# Serve static files (e.g. CSS, JS if needed)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

def simulate_neural_network_with_qiskit(plane_name, plane_type):
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    backend = AerSimulator()
    transpiled_qc = transpile(qc, backend)
    job = backend.run(transpiled_qc, shots=1)
    result = job.result().get_counts()
    key = list(result.keys())[0] if result else "00"
    neural_output = {
         "activation_message": f"{plane_name} ({plane_type}) activated!",
         "qiskit_simulation": f"Quantum output: {key}",
         "dynamic_content": "Trending topics in AI & Quantum Computing",
         "visualization": "<img src='https://via.placeholder.com/300x200.png?text=Data+Visualization' alt='Visualization'>",
         "instruction": "Enter commands to interact with the virtual grid..."
    }
    return neural_output

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
