from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import psycopg2 
from quantum_engine import run_basic_circuit # This line imports the function from the separate file

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/create_plane', methods=['POST'])
def create_plane():
    data = request.json
    plane_name = data.get('plane_name', 'Default Plane')
    plane_type = data.get('plane_type', 'Default Type')

    # Run the Qiskit simulation to get a "real" output from the quantum_engine.py file
    quantum_score = run_basic_circuit()

    # Placeholder for dynamic content from PostgreSQL
    # IMPORTANT: The connection details below have been updated with your provided values.
    topic = "AI & Quantum Computing (fallback)"
    try:
        conn = psycopg2.connect(
            dbname="imagination_portal",
            user="postgres",
            password="$9zZ28IQ",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT topic FROM trending_topics LIMIT 1;")
        if cursor.rowcount > 0:
            topic = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    except Exception as e:
        print("DB connection or query error:", e)

    return jsonify({
        "activation_message": f"{plane_name} ({plane_type}) activated!",
        "qiskit_simulation": f"Quantum output: {quantum_score}",
        "dynamic_content": f"Dynamic Data: Trending topic → {topic}",
        "visualization": "<img src='https://i.imgur.com/qvodtvv.png' alt='Visualization'>",
        "instruction": "Enter commands to interact with the virtual grid..."
    })

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
