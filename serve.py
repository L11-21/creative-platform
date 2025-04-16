from waitress import serve

from app import app  # Assumes your Flask app instance is named "app" in app.py

if __name__ == '__main__':
    # The host '0.0.0.0' makes it listen on all network interfaces.
    serve(app, host='0.0.0.0', port=5000)