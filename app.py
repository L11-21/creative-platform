from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import random
import psycopg2  # PostgreSQL connector
# from qiskit import QuantumCircuit, Aer, execute  # Uncomment when Qiskit is ready

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

    # 🔹 Placeholder for Qiskit simulation
    quantum_score = random.randint(80, 120)  # Replace with real Qiskit output later

    # 🔹 Placeholder for dynamic content from PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname="theme_lyftingv4_db",
            user="your_user",
            password="your_password",
            host="your_host",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT topic FROM trending_topics LIMIT 1;")
        topic = cursor.fetchone()[0] if cursor.rowcount > 0 else "AI & Quantum Computing"
        cursor.close()
        conn.close()
    except Exception as e:
        topic = "AI & Quantum Computing (fallback)"
        print("DB error:", e)

    return jsonify({
        "activation_message": f"{plane_name} ({plane_type}) activated!",
        "qiskit_simulation": f"Quantum Output: {quantum_score}",
        "dynamic_content": f"Dynamic Data: Trending topic → {topic}",
        "visualization": "<img src='https://i.imgur.com/qvodtvv.png' alt='Visualization'>",
        "instruction": "Enter commands to interact with the virtual grid..."
    })

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
