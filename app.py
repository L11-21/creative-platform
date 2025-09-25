import logging
import os
from urllib.parse import urlparse

import psycopg2
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

# Helper function to get a database connection
def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        result = urlparse(db_url)
        conn = psycopg2.connect(
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
    else:
        conn = psycopg2.connect(
            dbname="imagination_portal",
            user="postgres",
            password="$9zZ28IQ",
            host="localhost",
            port="5432"
        )
    return conn

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

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
