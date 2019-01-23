from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest

class TestStore(BaseTest):
  def test_create_store_items_empty(self):
    store = StoreModel('test_store')

    self.assertEqual(store.items.all(), [])

  def test_crud(self):
    with self.app_context():
      store = StoreModel('test')

      self.assertIsNone(StoreModel.find_by_name('test'))

      store.save_to_db()

      self.assertIsNotNone((StoreModel.find_by_name('test')))

      store.delete_from_db()

      self.assertIsNone(StoreModel.find_by_name('test'))

  def test_store_relationship(self):
    with self.app_context():
      store = StoreModel('test')
      item = ItemModel('test_item', 10.99, 1)

      store.save_to_db()
      item.save_to_db()

      self.assertEqual(store.items.count(), 1)
      self.assertEqual(store.items.first().name, 'test_item')

  def test_store_json(self):
    with self.app_context():
      store = StoreModel('test')
      item = ItemModel('test_item', 17.22, 1)

      store.save_to_db()
      item.save_to_db()

      self.assertDictEqual(store.json(), {'name': 'test', 'items': [{'name': 'test_item', 'price': 17.22}]})