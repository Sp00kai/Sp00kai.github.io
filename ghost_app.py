import os
import flask_cors
import waitress
from flask import Flask, jsonify, send_file

app = Flask(__name__)
flask_cors.CORS(app)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/run-code', methods=['POST'])
def run_code():
    result = "Python code executed!"
    return jsonify({'result': result})

def start_server():
    # Get port from environment variable or default to 8080
    port = int(os.environ.get('PORT', 4000))
    waitress.serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_server()