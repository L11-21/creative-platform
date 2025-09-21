import os

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# Serve index.html at root
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files (CSS, JS, images)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Handle form submission
@app.route('/create_plane', methods=['POST'])
def create_plane():
    data = request.json
    plane_name = data.get('plane_name', 'Default Plane')
    plane_type = data.get('plane_type', 'Default Type')
    return jsonify({
        "activation_message": f"{plane_name} ({plane_type}) activated!"
    })

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
