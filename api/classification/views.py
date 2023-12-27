from flask_restx import Namespace, Resource
from flask import request

# Create a namespace for image classification
classification_namespace = Namespace('classification', description='image classification')

@classification_namespace.route('/classify')
class Classify(Resource):
    #@classify_image_namespace.doc(responses={200: 'OK', 400: 'Bad Request'})
    def post(self):
        """
            classify image and save in database
        """
        # # Check if the request contains a file named 'image'
        # if 'image' not in request.files:
        #     return {"error": "No file provided"}, 400

        # # Access the uploaded file
        # image_file = request.files['image']

        # # Add your image classification logic here

        # return {"result": "Image classified successfully"}
        pass


@classification_namespace.route('/classification_results')
class GetUserClassificationResults(Resource):
    def get(self):
        """
            get classification results for a specific user
        """
        pass


@classification_namespace.route('/image/<string:image_file_name>')
class GetImage(Resource):
    #@classification_namespace.doc(responses={200: 'OK', 404: 'Image Not Found'})
    def get(self, image_file_name):
        """
            get image
        """
        # try:
        #     # Retrieve the image from the 'uploads' folder
        #     return send_from_directory(UPLOAD_FOLDER, image_file_name)
        # except FileNotFoundError:
        #     return {"error": "Image Not Found"}, 404
        pass


        
