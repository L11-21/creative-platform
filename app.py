from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

@app.route('/create_plane', methods=['POST'])
def create_plane():
    data = request.json
    return jsonify({"activation_message": f"{data.get('plane_name')} ({data.get('plane_type')}) activated!"})

if __name__ == '__main__':
    app.run(debug=True)
