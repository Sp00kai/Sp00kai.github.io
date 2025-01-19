import flask_cors
import waitress
from flask import Flask, jsonify, render_template

app = Flask(__name__)
flask_cors.CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-code', methods=['POST'])
def run_code():
    result = "Python code executed!"
    return jsonify({'result': result})

def start_server():
    waitress.serve(app, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    start_server()