from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

@app.route('/numbers', methods=['POST'])
def handle_post():
    json = request.json
    contents = base64.b64decode(json.loads(event['body'])['file-contents'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)