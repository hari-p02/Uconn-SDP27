from flask import Flask, request, jsonify
import subprocess
import base64
import requests

app = Flask(__name__)

folder_path = "/Users/haripat/Desktop/sdp/Uconn-SDP27/build_1/"

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
    if result.returncode == 0:
        print("Execution successful.")
        print("Output:", result.stdout)
    else:
        print("Execution failed.")
        print("Error:", result.stderr)
    
    

