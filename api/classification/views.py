import io
from flask_restx import Namespace, Resource
from flask import request
from http import HTTPStatus
from flask_cors import cross_origin
from ..models.classification_results import get_image_class_name


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

classification_namespace = Namespace('classification', description='image classification')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@classification_namespace.route('/classify')
class Classify(Resource):
    @cross_origin()
    def post(self):
        """Classify an image"""
        try:
            file = request.files.get('image')

            if file is None or file.filename == "":
                return {"error": "no file"}, HTTPStatus.BAD_REQUEST

            if not allowed_file(file.filename):
                return {"error": "invalid file extension"}, HTTPStatus.BAD_REQUEST

            image_data = io.BytesIO(file.read())
            image_class_name, probabilities = get_image_class_name(image_data)

            categories = ['Early Blight', 'Late Blight', 'Septoria Leaf Spot', 'Healthy']
            label_probabilities = {
                category: round(prob.item(), 4)
                for category, prob in zip(categories, probabilities[0])
            }

            return {
                'label': image_class_name,
                'label_probabilities': label_probabilities
            }, HTTPStatus.OK

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": "internal server error"}, HTTPStatus.INTERNAL_SERVER_ERROR
