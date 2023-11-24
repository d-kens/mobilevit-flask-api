from app import app
from model.classification_model import classification_model
from flask import request, send_file, jsonify
from utils.helper_functions import generate_image_filepath

classification_object = classification_model()

@app.route('/classify', methods=['POST'])
def predict_controller():
    # get uploaded image
    file = request.files.get('image')
    if file is None or file.filename == "":
        return jsonify({"error": "no file"})

    # generate filepath for the image
    filePath = generate_image_filepath(file)

    
    return classification_object.classify_image(file, filePath)
    