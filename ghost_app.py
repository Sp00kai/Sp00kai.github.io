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

@app.route('/chat')
def chat():
    return send_file('chat.html')

@app.route('/submit-assessment', methods=['POST'])
def submit_assessment():
    try:
        # Get the JSON data from the request
        assessment_data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'beliefScale', 'unexplainedResponse', 'paranormalInterest',
            'familyResponse', 'personalConnection', 'explorationComfort',
            'scientificBelief'
        ]
        
        for field in required_fields:
            if field not in assessment_data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Convert all values to strings for consistency
        response_data = {
            key: str(value) for key, value in assessment_data.items()
        }
        
        # Here you can add additional processing, storage, or analysis of the data
        # For now, we'll just return the processed data
        return jsonify({
            'message': 'Assessment submitted successfully',
            'data': response_data
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to process assessment',
            'details': str(e)
        }), 500

def start_server():
    # Get port from environment variable or default to 4000
    port = int(os.environ.get('PORT', 8080))
    waitress.serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    start_server()