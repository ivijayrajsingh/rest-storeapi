import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel
class RegisterUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="username can't be empty")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password can't be empty")
    def post(self):
        data = RegisterUser.parser.parse_args()
        if UserModel.find_user_by_name(data['username']):
            return {'message':'usere with that name exists'},400
        user = UserModel(data['username'],data['password'])
        user.save_to_db()
        return {'message':'registered succesfully'}, 201