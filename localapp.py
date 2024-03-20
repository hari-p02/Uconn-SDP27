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


