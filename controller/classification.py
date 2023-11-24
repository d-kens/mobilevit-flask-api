from app import app
from model.classification import classification
from flask import request, send_file, jsonify
from utils.helper_functions import generate_image_filepath

classification_object = classification()

@app.route('/classify', methods=['POST'])
def classify():
    # get uploaded image
    file = request.files.get('image')
    if file is None or file.filename == "":
        return jsonify({"error": "no file"})

    # generate filepath for the image
    filePath = generate_image_filepath(file)

    return classification_object.classify_image(file, filePath)
    