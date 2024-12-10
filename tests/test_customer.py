import unittest
from unittest.mock import patch
from factory_management.factory import create_app
from factory_management.models import Customer

class TestCustomerEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up the test client."""
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()  # Activate the app context
        self.client = self.app.test_client()

    def tearDown(self):
        """Tear down the test client."""
        self.app_context.pop()  # Remove the app context


    @patch('factory_management.models.Customer.query.all')
    def test_get_customers(self, mock_query):
        """Test retrieving all customers."""
        mock_query.return_value = [
            Customer(id=1, name="Jane Smith", email="jane@example.com", phone="1234567890"),
            Customer(id=2, name="Lane Smith", email="lane.smith@example.com", phone="2222222222")
        ]
        response = self.client.get('/api/customers')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Jane Smith", response.get_data(as_text=True))
        self.assertIn("Lane Smith", response.get_data(as_text=True))

    @patch('factory_management.models.db.session.add')
    @patch('factory_management.models.db.session.commit')
    def test_create_customer(self, mock_commit, mock_add):
        """Test creating a new customer."""
        response = self.client.post('/api/customers', json={
            "name": "Alice",
            "email": "alice@example.com",
            "phone": "1112223333"
        })
        self.assertEqual(response.status_code, 201)
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

    def test_get_customers_invalid_method(self):
        """Test accessing /api/customers with an invalid HTTP method."""
        response = self.client.post('/api/customers')  # POST is invalid for this endpoint
        self.assertIn(response.status_code, [400, 405])  # Accept both codes for now


if __name__ == '__main__':
    unittest.main()
