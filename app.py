import random

from flask import Flask, jsonify, render_template, request
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator  # Updated import

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_plane', methods=['POST'])
def create_plane():
    plane_name = request.form.get('plane_name', 'Default Plane')
    plane_type = request.form.get('plane_type', 'Default Type')
    neural_response = simulate_neural_network_with_qiskit(plane_name, plane_type)
    return jsonify(neural_response)

def simulate_neural_network_with_qiskit(plane_name, plane_type):
    # Create a simple quantum circuit
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Use the AerSimulator
    backend = AerSimulator()
    transpiled_qc = transpile(qc, backend)
    # Run the circuit directly with the backend's run() method without assemble()
    job = backend.run(transpiled_qc, shots=1)
    result = job.result().get_counts()
    key = list(result.keys())[0] if result else "00"

    # Compose and return the neural network response
    neural_output = {
         "activation_message": f"{plane_name} ({plane_type}) activated!",
         "qiskit_simulation": f"Quantum output: {key}",
         "dynamic_content": "Trending topics in AI & Quantum Computing",
         "visualization": "<img src='https://via.placeholder.com/300x200.png?text=Data+Visualization' alt='Visualization'>",
         "instruction": "Enter commands to interact with the virtual grid..."
    }
    return neural_output

if __name__ == '__main__':
    app.run(debug=True)