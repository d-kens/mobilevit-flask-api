from app import app
from flask import request, send_file, jsonify, make_response
from utils.helper_functions import generateImageFilepath
from model.imageClassification import imageClassification


imageClassifier = imageClassification()

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/classify-image', methods=['POST'])
def getImageClass():
    try:
        # get uploaded image
        file = request.files.get('image')
        if file is None or file.filename == "":
            return make_response(jsonify({"error": "no file"}), 400)

        if not allowed_file(file.filename):
            return make_response(jsonify({"error": "invalid file extension"}), 400)

        filepath = generateImageFilepath(file)
        
        # Save the image
        file.save(filepath)
        return imageClassifier.imageClass(filepath)
    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {e}")
        return make_response(jsonify({"error": "internal server error"}), 500)


# fetching the uploaded image
@app.route("/uploads/<filename>")
def get_uploaded_image(filename):
    try:
        return send_file(f"uploads/{filename}")
    except Exception as e:
        return "Error retrieving uploaded image", 500

