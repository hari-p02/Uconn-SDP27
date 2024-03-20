from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/numbers', methods=['POST'])
def handle_post():
    if request.is_json:
        json_data = request.get_json()

        print(json_data)

        return jsonify({"message": "Data received", "yourData": json_data}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)