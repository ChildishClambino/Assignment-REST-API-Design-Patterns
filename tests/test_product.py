import unittest
from unittest.mock import patch
from factory_management.factory import create_app
from factory_management.models import Product

class TestProductEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('factory_management.models.Product.query.all')
    def test_get_products(self, mock_query):
        mock_query.return_value = [
            Product(id=1, name="Widget", price=19.99)
        ]
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Widget", response.get_data(as_text=True))

    @patch('factory_management.models.db.session.add')
    @patch('factory_management.models.db.session.commit')
    def test_create_product(self, mock_commit, mock_add):
        response = self.client.post('/api/products', json={"name": "Gadget", "price": 29.99})
        self.assertEqual(response.status_code, 201)

    def test_get_products_invalid_method(self):
        response = self.client.post('/api/products')
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()
