from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_namespace = Namespace('auth', description="authentication")

register_model = auth_namespace.model(
    'User', {
        'firstname': fields.String(required=True, description="firstname"),
        'lastname': fields.String(required=True, description="lastname"),
        'username': fields.String(required=True, description="username"),
        'password':fields.String(required=True, description="password"),
    }
)

login_model = auth_namespace.model(
    'Login', {
        'username': fields.String(required=True, description="username"),
        'password': fields.String(required=True, description="password")
    }
)

@auth_namespace.route('/register')
class Register(Resource):
    
    @auth_namespace.expect(register_model)
    #@auth_namespace.marshal_with(register_model)
    def post(self):
        """
            create a new user account
        """
        try:
            data = request.get_json()

            # Check if the username already exists
            existing_user = User.query.filter_by(username=data.get('username')).first()
            if existing_user:
                return {'message': 'Username already exists. Please choose a different username.'}, HTTPStatus.CONFLICT

            # Create a new user
            user = User(
                firstname=data.get('firstname'),
                lastname=data.get('lastname'),
                username=data.get('username'),
                password=generate_password_hash(data.get('password'))
            )

            # Save the new user
            user.save()

            # Convert the user object to a dictionary representation
            user_dict = {
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'username': user.username,
            }

            return user_dict, HTTPStatus.CREATED
        
        except Exception as e:
            logging.exception('An error occurred during user registration:')
            return {'message': 'An error occurred while processing the request'}, HTTPStatus.INTERNAL_SERVER_ERROR


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
            generate jwt pair
        """
        try:
            data = request.get_json()

            username = data.get('username')
            password = data.get('password')

            user = User.query.filter_by(username=username).first()

            if (user is not None) and check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.username)
                refresh_token = create_refresh_token(identity=user.username)

                response = {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }

                return response, HTTPStatus.OK
            return {'message': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
        
        except Exception as e:
            # Log the exception or handle it appropriately
            return {'message': 'An error occurred while processing the request'}, HTTPStatus.INTERNAL_SERVER_ERROR


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
            refresh access token
        """
        username = get_jwt_identity()

        access_token = create_access_token(identity=username)

        return {
            'access_token': access_token
        }, HTTPStatus.OK

