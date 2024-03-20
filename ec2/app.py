from flask import Flask, request, jsonify
import base64
import subprocess

folder_path = "/home/ec2-user/server/build_2"

executable_name = "main"

executable_path = f"{folder_path}/{executable_name}"

app = Flask(__name__)

def read_file_into_base64_string(file_path):
    f = open(file_path,"rb")
    bin = f.read()
    return (base64.b64encode(bin)).decode('ascii')

@app.route('/numbers', methods=['POST'])
def handle_post():
    try:
        json = request.json
        for key in json.keys():
            contents = base64.b64decode(json[key])
            with open(f'/home/ec2-user/data/{key}.txt', 'wb') as file:
                file.write(contents)
        command = [executable_path]
        result = subprocess.run(command, capture_output=True, text=True, cwd=folder_path)
        payload = {
            "ciphertextAdd12": read_file_into_base64_string(folder_path + "/ciphertextAdd12.txt"),
        }
        return jsonify({"Suceess": "Calculation Occured", "result": payload}), 200
    except:
        return jsonify({}), 400

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)