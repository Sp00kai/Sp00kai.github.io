from flask import Flask, send_from_directory, request, redirect, url_for
from flask_cors import CORS
from waitress import serve
import os

app = Flask(__name__, static_url_path='')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat')
def chat():
    return send_from_directory('.', 'chat.html')

@app.route('/ghost_persona')
def ghost_persona():
    return send_from_directory('.', 'ghost_persona.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

@app.route('/submit-assessment', methods=['POST'])
def submit_assessment():
    try:
        # Get the form data
        data = request.get_json()
        
        # Store the ghost persona in session storage (this will be handled by JavaScript)
        # Just redirect to chat page
        return {'redirect': '/chat'}, 200
        
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    print("Server starting on http://localhost:8080")
    serve(app, host='0.0.0.0', port=8080) 