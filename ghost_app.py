import os
import flask_cors
import waitress
from flask import Flask, jsonify, send_file, request

app = Flask(__name__)
# Configure CORS with additional options
flask_cors.CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/run-code', methods=['POST', 'OPTIONS'])
def run_code():
    if request.method == 'OPTIONS':
        return '', 200
    result = "Python code executed!"
    app.logger.info(f"Received request: {request.json}")
    print("Received request: ", request.json)
    return jsonify({'result': result})

def start_server():
    # Get port from environment variable or default to 4000
    port = int(os.environ.get('PORT', 4000))
    waitress.serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_server()