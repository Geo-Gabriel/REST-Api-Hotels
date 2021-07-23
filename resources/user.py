from operator import imod, ne
from flask_jwt_extended.utils import get_raw_jwt
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp
from models.user import UserModel, get_uuid
from blacklist import BLACKLIST
import datetime

from database.sql_alchemy import db

attr = reqparse.RequestParser()
username = attr.add_argument('username', type=str, required=True, help="The field 'username' cannot be left blank.")
password = attr.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank.")


class Users(Resource):
    def get(self):
        # return insert_data()
        all_users = [user.json() for user in UserModel.query.all()]
        return {
            "query_datetime": str(datetime.datetime.now()),
            "users_in_database": len(all_users),
            "users": all_users
            }

class User(Resource):
    # /users/{user_id}
    def get(self, user_id: str) -> dict:
        user = UserModel.find_user(user_id=user_id)
        if user:
            return user.json(), 200
        return {'message': f"user id '{user_id}' not found"}, 404  # not found
    
    @jwt_required
    def delete(self, user_id: str) -> dict:
        user = UserModel.find_user(user_id=user_id)
        if user:
            try:
                user.delete()
            except:
                return {'message': 'An internal error ocurred trying to delete user'}, 500  # internal server error
            return {'message': f"User '{user.username}' deleted."}, 200
        return {'message': f"User id: '{user_id}' not found."}, 404

class UserRegister(Resource):
    # /register
    def post(self):
        user_data = attr.parse_args()  # get the data
        if UserModel.find_user_by_username(username=user_data['username']):
            return {"message": f"The username '{user_data['username']}' already exists."}, 400
        
        new_user = UserModel(**user_data)  # create new User obj

        try:
            new_user.save()
        except:
            return {'message': 'An internal error ocurred trying to save user'}, 500  # internal server error
        return {'message': f"User '{user_data['username']}' succesfully created."}, 201

class UserLogin(Resource):
    def post(cls):
        data = attr.parse_args()
        user = UserModel.find_user_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.user_id)
            return {'access_token': access_token}, 200

        return {'message': 'The username or password is incorrect.'}, 401  # Unautorized

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']  #JTI - JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': "Logged out successfully"}, 200
