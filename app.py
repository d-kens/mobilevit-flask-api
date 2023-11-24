from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
    return "MobileViT for tomato crop disease classification"

from controller import *

