import logging
import psycopg2
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

# Direct connection to Render-hosted PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        dbname="codex_sync_db",
        user="codex_sync_db_user",
        password="KfunTyRtyuVHJK0Mnoxat3h0ZOQSdYbQ",
        host="dpg-d35onb8dl3ps739404ug-a.virginia-postgres.render.com",
        port="5432"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"db_status": "connected"}), 200
    except Exception as e:
        logging.error(f"Status check failed: {e}")
        return jsonify({"db_status": "error"}), 500

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/submit-plane', methods=['POST'])
def submit_plane():
    data = request.get_json()
    plane_name = data.get('plane_name')
    plane_type = data.get('plane_type')

    if not plane_name or not plane_type:
        return jsonify({"error": "Both plane_name and plane_type are required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO plane_registry (plane_name, plane_type) VALUES (%s, %s)",
            (plane_name, plane_type)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Plane entry submitted successfully"}), 201
    except Exception as e:
        logging.error(f"Insertion failed: {e}")
        return jsonify({"error": "Database insertion failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)
