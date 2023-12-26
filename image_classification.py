from flask import Blueprint, jsonify, request, make_response
from models import ClassificationResult
import os

classification_blueprint = Blueprint('classification', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@classification_blueprint.post('/classify-image')
def classify_image():
    try:
        file = request.files.get('image')

        if file is None or file.filename == "":
            return make_response(jsonify({"error": "no file"}), 400)

        if not allowed_file(file.filename):
            return make_response(jsonify({"error": "invalid file extension"}), 400)

        # Generate file path
        file_path = ClassificationResult.generate_image_filepath(file)
        file.save(file_path)

        # get image class index
        image_class_name = ClassificationResult.get_image_class_name(file_path)

        # save image in the database

        # return response
        filename = os.path.basename(file_path)

        return jsonify({
            'label': image_class_name,
            'filename': filename
        })

    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {e}")
        return make_response(jsonify({"error": "internal server error"}), 500)