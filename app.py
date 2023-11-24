from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def welcome():
    return "Welcome to rmobileViT inference api"

from controller import *

