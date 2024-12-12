import unittest
from unittest.mock import patch, MagicMock
from factory_management.factory import create_app

class TestOrderEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('factory_management.models.Order.query')  # Adjusted to patch the query object
    def test_get_orders(self, mock_query):
        """Test retrieving all orders."""
        # Mocking orders
        mock_order = MagicMock()
        mock_order.to_dict.return_value = {
            "id": 1,
            "customer_id": 1,
            "product_id": 1,
            "quantity": 2,
            "total_price": 40.0
        }
        mock_query.all.return_value = [mock_order]

        # Debug: Verify the mock setup
        print("Mock query setup:", mock_query.all.return_value)

        # Send a GET request
        response = self.client.get('/api/orders/')
        print(f"Response status: {response.status_code}")
        response_data = response.get_json()
        print(f"Response data: {response_data}")

        # Assertions
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
        self.assertEqual(len(response_data), 1, f"Expected 1 order, got {len(response_data)}")
        self.assertDictEqual(response_data[0], {
            "id": 1,
            "customer_id": 1,
            "product_id": 1,
            "quantity": 2,
            "total_price": 40.0
        })

        # Assert the mock was called
        mock_query.all.assert_called_once()

if __name__ == '__main__':
    unittest.main()
