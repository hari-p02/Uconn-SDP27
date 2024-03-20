from flask import Flask, request, jsonify
import subprocess
import base64
import requests

app = Flask(__name__)

folder_path = "/Users/haripat/Desktop/sdp/Uconn-SDP27/build_1"

executable_name = "main"

executable_path = f"{folder_path}/{executable_name}"

def read_file_into_base64_string(file_path):
    f = open(file_path,"rb")
    bin = f.read()
    return (base64.b64encode(bin)).decode('ascii')

def serilize(x, y):
    args = [x, y]
    command = [executable_path] + args
    result = subprocess.run(command, capture_output=True, text=True, cwd=folder_path)
    print(result)
    if result.returncode == 0:
        print("Execution successful.")
        print("Output:", result.stdout)
    else:
        print("Execution failed.")
        print("Error:", result.stderr)
    
@app.route('/serilize', methods=['POST'])
def handle_post():
    try:
        json = request.json
        x, y = json['x'], json['y']
        print("here")
        serilize(x, y)
        print("here")
        payload = {
            "ciphertext1": read_file_into_base64_string(folder_path + "/ciphertext1.txt"),
            "ciphertext2": read_file_into_base64_string(folder_path + "/ciphertext2.txt"),
            "key-eval-rot": read_file_into_base64_string(folder_path + "/key-eval-rot.txt"),
            "key-public": read_file_into_base64_string(folder_path + "/key-public.txt"),
            "cryptocontext": read_file_into_base64_string(folder_path + "/cryptocontext.txt"),
            "key-eval-mult": read_file_into_base64_string(folder_path + "/key-eval-mult.txt")
        }

        requests.post("http://ec2-52-91-147-180.compute-1.amazonaws.com:5000/numbers", json=payload)
        return jsonify({"message": "Data sent"}), 200
    except:
        return jsonify({"error": "Failure Occured"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)