from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest

class TestStore(UnitBaseTest):
  def test_create_store(self):
    store = StoreModel('test_store')

    self.assertEqual(store.name, 'test_store')


  def test_json_store(self):
    store = StoreModel('test_store')

    self.assertDictEqual(store.json(), {'name': 'test_store', 'items': []})