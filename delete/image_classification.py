from flask import Blueprint, jsonify, request, make_response, send_file
from models import ClassificationResult
import os

classification_blueprint = Blueprint('classification', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@classification_blueprint.post('/classify')
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
        classification_result = ClassificationResult(
            image_path = file_path,
            result_value = image_class_name,
            user_id = 1
        )

        classification_result.save()

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


@classification_blueprint.get('/previous_results')
def get_previous_results():
    try:
        # ! Should implemt logic for getting current user id
        user_id = 1

        # Assuming you have a method in your model to retrieve results by user ID
        previous_results = ClassificationResult.get_results_by_user_id(user_id)

        print(previous_results)

        # Check if any results were found
        if not previous_results:
            return make_response(jsonify({"error": "no results found for the user"}), 404)

        
       # Construct a list of results with image_path, result_value, and timestamp
        results_list = [
            {
                'filename': os.path.basename(result.image_path),
                'result_value': result.result_value,
                'timestamp': result.timestamp.isoformat()  # Convert timestamp to ISO format
            }
            for result in previous_results
        ]

        return jsonify({"previous_results": results_list})

    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {e}")
        return make_response(jsonify({"error": "internal server error"}), 500)


# Add this route to the existing blueprint
@classification_blueprint.get('/get_image/<filename>')
def get_image(filename):
    try:
        image_path = os.path.join('uploads', filename)

        # Check if the file exists
        if not os.path.isfile(image_path):
            return make_response(jsonify({"error": "image not found"}), 404)

        # Send the file in the response
        return send_file(image_path, mimetype='image/jpeg')

    except Exception as e:
        # Log the exception for debugging
        print(f"An error occurred: {e}")
        return make_response(jsonify({"error": "internal server error"}), 500)
