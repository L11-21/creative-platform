import logging
import os
from urllib.parse import urlparse

import psycopg2
from flask import Flask, jsonify, send_from_directory
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

if __name__ == '__main__':
    app.run(debug=True)
