from models.user import UserModel
from tests.base_test import BaseTest
import json

class UserTest(BaseTest):
  def test_register_user(self):
    with self.app() as client:
      with self.app_context():
        response = client.post('/register', data={'username': 'user1', 'password': '1234'})

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(UserModel.find_by_username('user1'))
        self.assertDictEqual({'message': 'User registered successfully'}, json.loads(response.data))

  def test_login_user(self):
    with self.app() as client:
      with self.app_context():
        client.post('/register', data={'username': 'user1', 'password': '1234'})
        auth_response = client.post('/auth',
                                   data=json.dumps({'username': 'user1', 'password': '1234'}),
                                                   headers={'Content-Type': 'application/json'})

        self.assertIn('access_token', json.loads(auth_response.data).keys())

  def test_register_duplicate_user(self):
    with self.app() as client:
      with self.app_context():
        user = UserModel('user1', '1234')
        user.save_to_db()
        response = client.post('/register', data={'username': 'user1', 'password': '1234'})

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual({'message': 'Already existing user with this username'}, json.loads(response.data))