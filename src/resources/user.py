from flask_restful import Resource, reqparse

from models import User as UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help='This field cannot be blank'
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help='This field cannot be blank'
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']) is not None:
            return dict(message='A user with that username already exists'), 400

        user = UserModel(**data)

        try:
            user.save()
        except:
            return dict(message="An error occurred inserting the user"), 500

        return dict(message='User created successfully'), 201