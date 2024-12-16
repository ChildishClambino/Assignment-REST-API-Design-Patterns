import unittest
from unittest.mock import patch, MagicMock
from factory_management.factory import create_app
from factory_management.models import Product


class TestProductEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('factory_management.utils.util.decode_token')  # Mock the token decoding function
    @patch('factory_management.models.Product.query.all')
    def test_get_products(self, mock_query_all, mock_decode_token):
        mock_decode_token.return_value = {'sub': 1, 'role': 'user'}  # Mock decoded token payload
        mock_query_all.return_value = [
            MagicMock(id=1, name="Widget", price=19.99)
        ]
        headers = {'Authorization': 'Bearer mock_token'}
        response = self.client.get('/api/products', headers=headers)
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.get_json()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Widget", response.get_data(as_text=True))

    @patch('factory_management.utils.util.decode_token')  # Mock the token decoding function
    @patch('factory_management.models.db.session.add')
    @patch('factory_management.models.db.session.commit')
    def test_create_product(self, mock_commit, mock_add, mock_decode_token):
        mock_decode_token.return_value = {'sub': 1, 'role': 'admin'}  # Mock decoded token payload
        headers = {'Authorization': 'Bearer mock_token'}
        response = self.client.post('/api/products', json={"name": "Gadget", "price": 29.99}, headers=headers)
        print(f"Create product response status: {response.status_code}")
        print(f"Create product response data: {response.get_json()}")
        self.assertEqual(response.status_code, 201)

    def test_get_products_invalid_method(self):
        """
        Test accessing /api/products with an invalid HTTP method. 
        This skips role validation to directly check for 405.
        """
        response = self.client.put('/api/products')  
        print(f"Invalid method response status: {response.status_code}")
        self.assertEqual(response.status_code, 405) 


if __name__ == '__main__':
    unittest.main()
