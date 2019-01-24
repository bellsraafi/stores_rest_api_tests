import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest

class StoreTest(BaseTest):
  def test_create_store(self):
    with self.app() as client:
      with self.app_context():
        response = client.post('/store/test_store')

        self.assertEqual(201, response.status_code)
        self.assertIsNotNone(StoreModel.find_by_name('test_store'))
        self.assertDictEqual({'id': 1, 'name': 'test_store', 'items': []}, json.loads(response.data))

  def test_create_duplicate_store(self):
    def test_create_store(self):
      with self.app() as client:
        with self.app_context():
          store_name = 'test_store'
          store = StoreModel(store_name)
          store.save_to_db()
          response = client.post(f'/store/{store_name}')

          self.assertEqual(400, response.status_code)
          self.assertDictEqual({'message': f'A store with name {store_name} already exists.'})

  def test_delete_store(self):
    with self.app() as client:
      with self.app_context():
        store_name = 'test_store'
        store = StoreModel(store_name)
        store.save_to_db()
        response = client.delete(f'/store/{store_name}')

        self.assertEqual(200, response.status_code)

  def test_find_store(self):
    with self.app() as client:
      with self.app_context():
        store_name = 'test_store'
        store = StoreModel(store_name)
        store.save_to_db()
        response = client.get(f'/store/{store_name}')

        self.assertEqual(200, response.status_code)
        self.assertDictEqual({'id': 1, 'name': 'test_store', 'items': []}, json.loads(response.data))

  def test_store_not_found(self):
    with self.app() as client:
      with self.app_context():
        response = client.get('/store/helloworld')

        self.assertEqual(404, response.status_code)
        self.assertDictEqual({'message': 'Store not found'}, json.loads(response.data))

  def test_store_found_with_items(self):
    with self.app() as client:
      with self.app_context():
        store_name = 'test_store'
        store = StoreModel(store_name).save_to_db()
        item = ItemModel('test_item', 17.45, 1).save_to_db()

        response = client.get(f'/store/{store_name}')

        self.assertEqual(200, response.status_code)
        self.assertDictEqual({'id': 1, 'name': store_name, 'items': [{'name': 'test_item', 'price': 17.45}]}, json.loads(response.data))


  def test_store_list(self):
    with self.app() as client:
      with self.app_context():
        store_name = 'test_store'
        store = StoreModel(store_name).save_to_db()

        response = client.get('/stores')

        self.assertDictEqual({'stores': [{'id': 1, 'name': store_name, 'items': []}]}, json.loads(response.data))

  def test_store_list_with_items(self):
    with self.app() as client:
      with self.app_context():
        store_name = 'test_store'
        store = StoreModel(store_name).save_to_db()
        item = ItemModel('test_item', 17.45, 1).save_to_db()

        response = client.get('/stores')

        self.assertDictEqual({'stores': [{'id': 1, 'name': store_name, 'items': [{'name': 'test_item', 'price': 17.45}]}]},
                             json.loads(response.data))