import os
from flask_restx import Namespace, Resource
from flask import request, send_file
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from ..models.classification_results import ClassificationResult
from ..models.users import User
from math import ceil


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


# Create a namespace for image classification
classification_namespace = Namespace('classification', description='image classification')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@classification_namespace.route('/classify')
class Classify(Resource):
    @cross_origin()
    @jwt_required()
    def post(self):
        """
            Classify image and save in database
        """
        try:
            file = request.files.get('image')

            if file is None or file.filename == "":
                return {"error": "no file"}, HTTPStatus.BAD_REQUEST

            if not allowed_file(file.filename):
                return {"error": "invalid file extension"}, HTTPStatus.BAD_REQUEST

            # Generate file path
            file_path = ClassificationResult.generate_image_filepath(file)
            file.save(file_path)

            # get image class name
            image_class_name, probabilities = ClassificationResult.get_image_class_name(file_path)

            # get user id - Uncomment Later
            username = get_jwt_identity()
            current_user = User.query.filter_by(username=username).first()
            user_id = current_user.id
             

            # save image in the database
            classification_result = ClassificationResult(
                image_path = file_path,
                result_value = image_class_name,
                user_id = user_id
            )

            classification_result.save()

            # construct URL for the image
            server_url = request.url_root.rstrip('/')
            image_url = f"{server_url}/{file_path}"

            
            # get class probabilities
            categories = ['Early Blight', 'Late Blight', 'Septoria Leaf Spot', 'Healthy']
            label_probabilities = {category: round(probability.item(), 4) for category, probability in zip(categories, probabilities[0])}
            

            return {
                'label': image_class_name,
                'image_url':  image_url,
                'label_probabilities': label_probabilities
            }, HTTPStatus.OK
        
        except Exception as e:
            # Log the exception for debugging
            print(f"An error occurred: {e}")
            return {"error": "internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR



@classification_namespace.route('/classification_results/<int:user_id>')
class GetUserClassificationResults(Resource):
    @cross_origin()
    @jwt_required()
    def get(self, user_id):
        """
            Get classification results for a specific user
        """
        try:
            # check if user exists
            user=User.get_by_id(user_id)
            if not user:
                return {
                    "error": "user not found"
                }, HTTPStatus.NOT_FOUND

            # query for results
            results = ClassificationResult.get_results_by_user_id(user_id)

            if not results:
                return {
                    "message": "No previous classification results"
                }, HTTPStatus.NO_CONTENT

            

            # Get pagination parameters from the request
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=2, type=int)

            total_pages = ceil(len(results) / per_page)

            # Paginate the results
            paginated_results = results[(page - 1) * per_page: page * per_page]

            # Construct a list of results with image_path, result_value, and timestamp
            results_list = [
                {
                    'image_url': self.get_image_url(result.image_path),
                    'result_value': result.result_value,
                    'timestamp': result.timestamp.isoformat() 
                }
                for result in paginated_results
            ]

            response_data = {
                'results': results_list,
                'total_pages': total_pages
            }


            return response_data, HTTPStatus.OK
        
        except Exception as e:
            # Log the exception for debugging
            print(f"An error occurred: {e}")
            return {"error": "internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR


    def get_image_url(self, image_path):
        # Construct the URL for the image
        server_url = request.url_root.rstrip('/')
        image_url = f"{server_url}/{image_path}"
        return image_url



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
