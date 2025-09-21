from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/create_plane', methods=['POST'])
def create_plane():
    data = request.json
    plane_name = data.get('plane_name', 'Default Plane')
    plane_type = data.get('plane_type', 'Default Type')

    return jsonify({
        "activation_message": f"{plane_name} ({plane_type}) activated!",
        "qiskit_simulation": "Quantum output: 101",
        "dynamic_content": "Dynamic Data: Trending topics in AI & Quantum Computing",
        "visualization": "<img src='https://i.imgur.com/qvodtvv.png' alt='Visualization'>",
        "instruction": "Enter commands to interact with the virtual grid..."
    })

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
