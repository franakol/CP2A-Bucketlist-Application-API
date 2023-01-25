from api.config.config import config
from flask_restx import Namespace,Resource,fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash,check_password_hash
from http import HTTPStatus
from flask_jwt_extended import (create_access_token,
create_refresh_token,jwt_required,get_jwt_identity)
from datetime import datetime



auth_namespace=Namespace('auth',description="a namespace for authentication")

register_model=auth_namespace.model(
    'Register', {
        'user_id':fields.Integer(),
        'username':fields.String(required=True,description="A username"),
        'email':fields.String(required=True,description="User email"),
        'password':fields.String(required=True,description="User password"),
        'date_created':fields.DateTime(required=True,description="date of creation"),
        'date_modified':fields.DateTime(required=True,description="date of modification")


    }
)

user_model=auth_namespace.model(
    'User', {
        'user_id':fields.Integer(),
        'username':fields.String(required=True,description="A username"),
        'email':fields.String(required=True,description="An email"),
        'password':fields.String(required=True,description="A password"),
        'date_created':fields.DateTime(required=True,description="date of creation"),
        'date_modified':fields.DateTime(required=True,description="date of modification")


    }
)


login_model=auth_namespace.model(
    'Login',{
        'email':fields.String(required=True,description="An email"),
        'password':fields.String(required=True,description="A password")
    }
)


@auth_namespace.route('/register')
class Register(Resource):

    @auth_namespace.expect(register_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
           Register a user
        """
        
        data = request.get_json()
        """
           returns data in json
        """        


        new_user=User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash( data.get('password')),
            date_created=data.get('date_created'),
            date_modified=data.get('date_modified')

        )


        new_user.save()

        return new_user , HTTPStatus.CREATED


@auth_namespace.route('/login')
class Login(Resource):

    @auth_namespace.expect(login_model)
    def post(self):


        """
           Logs a user in, generates jwt token
        """

        data=request.get_json()


        email=data.get('email')
        password=data.get('password')

        user=User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password,password):


            access_token=create_access_token(identity=user.username)
            refresh_token=create_refresh_token(identity=user.username)

            response={
                'access_token':access_token,
                'refresh_token':refresh_token
            }

            print("response")
            return response, HTTPStatus.OK
