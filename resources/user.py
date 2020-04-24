import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token,create_refresh_token

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                        type=str,
                        required=True,
                        help="username can't be empty")
_user_parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password can't be empty")


class RegisterUser(Resource):

    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_user_by_name(data['username']):
            return {'message':'usere with that name exists'},400
        user = UserModel(data['username'],data['password'])
        user.save_to_db()
        return {'message':'registered succesfully'}, 201


class User(Resource):

    def __init__(self,name):
        self.name = name

    @classmethod
    def get(cls,user_id):
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {'message':'user not found'},404
        return user.json


    @classmethod
    def delete(cls,user_id):
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {'message':'user doesnot exist'}
        user.delete_from_db()
        return {'message':'user got deleted'},200

class UserLogin(Resource):

    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_user_by_name(data['name'])

        # this is what the authenticate function does
        if user and safe_str_cmp(user.password,data['password']):
            # this is what the identity function does
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            },200
        return {'message':'user not found'},401