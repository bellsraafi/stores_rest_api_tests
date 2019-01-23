from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
  """
  This Resource allow users to register by sending a
  POST request with username and password
  """

  parser = reqparse.RequestParser()
  parser.add_argument('username',
                      type=str,
                      required=True,
                      help='The field cannot be blank')
  parser.add_argument('password',
                      type=str,
                      required=True,
                      help='This field cannot be blank')

  def post(self):
    data = UserRegister.parser.parse_args()

    if UserModel.find_by_username(data['username']):
      return {'message': 'Already existing user with this username'}, 400

    user = UserModel(**data)
    user.save_to_db()

    return {'message': 'User registered successfully'}, 201

  def delete(self):
    data = UserRegister.parser.parse_args()

    user = UserModel.find_by_username(data['username'])
    if user:
      user.delete_from_db(self)

    return {'message': 'User deleted'}


class UserDelete(Resource):
  def delete(self):
    data = UserDelete.parser.parse_args()

    user = UserModel.find_by_username(data['username'])
    if user:
      user.delete_from_db(self)

    return {'message': 'User deleted'}