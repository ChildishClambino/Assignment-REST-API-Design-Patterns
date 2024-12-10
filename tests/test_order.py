import unittest
from unittest.mock import patch
from factory_management.factory import create_app
from factory_management.models import Order

class TestOrderEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('factory_management.models.Order.query.all')
    def test_get_orders(self, mock_query):
        mock_query.return_value = [
            Order(id=1, customer_id=1, product_id=1, quantity=10, total_price=100.0)
        ]
        response = self.client.get('/api/orders')
        self.assertEqual(response.status_code, 200)
        self.assertIn("100.0", response.get_data(as_text=True))

    @patch('factory_management.models.db.session.add')
    @patch('factory_management.models.db.session.commit')
    def test_create_order(self, mock_commit, mock_add):
        response = self.client.post('/api/orders', json={"customer_id": 1, "product_id": 1, "quantity": 2, "total_price": 40.0})
        self.assertEqual(response.status_code, 201)

    def test_get_orders_invalid_method(self):
        response = self.client.post('/api/orders')
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()
