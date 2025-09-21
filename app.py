import os
import random

import psycopg2
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)  # Enable CORS if frontend is served separately

# 🔧 PostgreSQL Database Configuration
DB_CONFIG = {
    "dbname": "your_db_name",
    "user": "your_db_user",
    "password": "your_db_password",
    "host": "localhost",  # or your remote host
    "port": "5432"
}

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/create_plane', methods=['POST'])
def create_plane():
    data = request.json
    plane_name = data.get('plane_name', 'Default Plane')
    plane_type = data.get('plane_type', 'Default Type')

    # Simulated quantum-style response
    activation_message = f"<span class='math-inline'>{plane_name}</span> ({plane_type}) activated!"
    qiskit_simulation = f"Quantum output: {random.choice(['101', '110', '011'])}"
    dynamic_content = "Dynamic Data: Trending topics in AI & Quantum Computing"
    visualization = "<img src='https://i.imgur.com/qvodtvv.png' alt='Visualization'>"
    instruction = "Enter commands to interact with the virtual grid..."

    response = {
        "activation_message": activation_message,
        "qiskit_simulation": qiskit_simulation,
        "dynamic_content": dynamic_content,
        "visualization": visualization,
        "instruction": instruction
    }

    return jsonify(response)

@app.route('/execute_command', methods=['POST'])
def execute_command():
    data = request.json
    command = data.get('command', '')

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(command)

        if cur.description:  # SELECT query
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            result = [dict(zip(columns, row)) for row in rows]
            output = f"Query returned {len(result)} rows:\n" + str(result)
        else:  # INSERT/UPDATE/DELETE
            conn.commit()
            output = f"Command executed successfully: {command}"

        cur.close()
        conn.close()

    except Exception as e:
        output = f"[Database Error]: {str(e)}"

    return jsonify({ "output": output })

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
