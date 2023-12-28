import os
from flask_restx import Namespace, Resource
from flask import request, send_file
from ..models.classification_results import ClassificationResult
from ..models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity


## Allowed Image Extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create a namespace for image classification
classification_namespace = Namespace('classification', description='image classification')

@classification_namespace.route('/classify')
class Classify(Resource):
    #@classify_image_namespace.doc(responses={200: 'OK', 400: 'Bad Request'})
    #@jwt_required()
    def post(self):
        """
            classify image and save in database
        """
        try:
            file = request.files.get('image')

            if file is None or file.filename == "":
                return make_response(jsonify({"error": "no file"}), 400)

            if not allowed_file(file.filename):
                return make_response(jsonify({"error": "invalid file extension"}), 400)

            # Generate file path
            file_path = ClassificationResult.generate_image_filepath(file)
            file.save(file_path)

            # get image class name
            image_class_name = ClassificationResult.get_image_class_name(file_path)

            #! # get user id - Uncomment Later
            # username = get_jwt_identity()
            # current_user = User.query.filter_by(username=username).first()
            # user_id = current_user.id
             

            # save image in the database
            classification_result = ClassificationResult(
                image_path = file_path,
                result_value = image_class_name,
                user_id = 1
            )

            classification_result.save()

            # return response
            filename = os.path.basename(file_path)

            return {
                'label': image_class_name,
                'filename': filename
            }, HTTPStatus.OK
        
        except Exception as e:
            # Log the exception for debugging
            print(f"An error occurred: {e}")
            return {"error": "internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR




@classification_namespace.route('/image/<string:image_file_name>')
class GetImage(Resource):
    def get(self, image_file_name):
        """
            request an image file using the image name
        """
        try:
            # Assuming your Flask app is in a directory named "api"
            app_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            image_path = os.path.join(app_directory, 'uploads', image_file_name)

            print(image_path)

            # Check if the file exists
            if not os.path.isfile(image_path):
                return {"error": "image not found"}, HTTPStatus.NOT_FOUND

            # Send the file in the response
            return send_file(image_path, mimetype='image/jpeg')


        except Exception as e:
            # Log the exception for debugging
            print(f"An error occurred: {e}")
            return {"error": "internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR



@classification_namespace.route('/classification_results/<int:user_id>')
class GetUserClassificationResults(Resource):
    def get(self, user_id):
        """
            get classification results for a specific user
        """
        try:
            user=User.get_by_id(user_id)

            if not user:
                return {
                    "error": "user not found"
                }, HTTPStatus.NOT_FOUND

            results = ClassificationResult.get_results_by_user_id(user_id)

            if not results:
                return {
                    "message": "no previous classificatio results"
                }, HTTPStatus.NO_CONTENT

            # Construct a list of results with image_path, result_value, and timestamp
            results_list = [
                {
                    'filename': os.path.basename(result.image_path),
                    'result_value': result.result_value,
                    'timestamp': result.timestamp.isoformat()  # Convert timestamp to ISO format
                }
                for result in results
            ]


            return results_list, HTTPStatus.OK
        
        except Exception as e:
            # Log the exception for debugging
            print(f"An error occurred: {e}")
            return {"error": "internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR


