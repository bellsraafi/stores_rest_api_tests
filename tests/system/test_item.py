from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json

class TestItem(BaseTest):
  def setUp(self):
    super(TestItem, self).setUp()
    with self.app() as client:
      with self.app_context():

        UserModel('user1', '1234').save_to_db()
        StoreModel('fruit').save_to_db()
        ItemModel('guava', 17.22, 1).save_to_db()
        auth_response = client.post('/auth',
                                    data=json.dumps({'username': 'user1', 'password': '1234'}),
                                    headers={'Content-Type': 'application/json'})
        self.access_token = f"JWT {json.loads(auth_response.data)['access_token']}"

  def test_get_item_no_auth(self):
    with self.app() as client:
      with self.app_context():
        response = client.get('/item/guava')

        self.assertEqual(400, response.status_code)


  def test_get_item_not_found(self):
    with self.app() as client:
      with self.app_context():
        header = {'Authorization': self.access_token}
        response = client.get('/item/agbalumo', headers=header)

        self.assertEqual(404, response.status_code)

  def test_get_item(self):
    with self.app() as client:
      with self.app_context():
        header = {'Authorization': self.access_token}
        response = client.get('/item/guava', headers=header)

        self.assertEqual(200, response.status_code)
        self.assertDictEqual({'name': 'guava', 'price': 17.22}, json.loads(response.data))

  def test_delete_item(self):
    with self.app() as client:
      with self.app_context():
        response = client.delete('/item/guava')

        self.assertEqual(200, response.status_code)
        self.assertIsNone(ItemModel.find_by_name('guava'))
        self.assertDictEqual({'message': 'Item deleted'}, json.loads(response.data))

  def test_create_item(self):
    with self.app() as client:
      with self.app_context():
        response = client.post('/item/grape', data={'price': 17.22, 'store_id': 1})

        self.assertEqual(201, response.status_code)
        self.assertDictEqual({'name': 'grape', 'price': 17.22}, json.loads(response.data))

  def test_create_duplicate_item(self):
    with self.app() as client:
      with self.app_context():
        ItemModel('grape', 16.04, 1).save_to_db()
        response = client.post('/item/grape', data={'price': 16.04, 'store_id': 1})

        self.assertEqual(400, response.status_code)
        self.assertDictEqual({'message': "An item with name 'grape' already exists."}, json.loads(response.data))

  def test_put_item(self):
    with self.app() as client:
      with self.app_context():

        self.assertIsNone(ItemModel.find_by_name('carrot'))

        response = client.put('/item/carrot', data={'price': 16.04, 'store_id': 1})

        self.assertEqual(200, response.status_code)
        self.assertDictEqual({'name': 'carrot', 'price': 16.04}, json.loads(response.data))

  def test_put_update_item(self):
    with self.app() as client:
      with self.app_context():

        self.assertIsNotNone(ItemModel.find_by_name('guava'))

        response = client.put('/item/guava', data={'price': 16.04, 'store_id': 1})

        self.assertEqual(200, response.status_code)
        self.assertDictEqual({'name': 'guava', 'price': 16.04}, json.loads(response.data))

  def test_item_list(self):
    with self.app() as client:
      with self.app_context():
        response = client.get('/items')

        self.assertEqual(200, response.status_code)
        self.assertDictEqual({'items': [{'name': 'guava', 'price': 17.22}]}, json.loads(response.data))
