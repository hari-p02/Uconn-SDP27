from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

@app.route('/numbers', methods=['POST'])
def handle_post():
    try:
        json = request.json
        for key in json.keys():
            contents = base64.b64decode(json[key])
            with open(f'/home/ec2-user/data/{key}.txt', 'wb') as file:
                file.write(contents)
        return jsonify({}), 200
    except:
        return jsonify({}), 400

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)