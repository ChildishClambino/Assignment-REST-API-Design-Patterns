import unittest
from unittest.mock import patch, MagicMock
from factory_management.factory import create_app
from factory_management.models import Production
from datetime import datetime

class TestProductionEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and application context."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()  # Push the application context for testing

    def tearDown(self):
        """Tear down the application context."""
        self.app_context.pop()

    @patch('factory_management.models.Production.query')
    def test_get_productions(self, mock_query):
        """Test retrieving all production records."""
        # Mock the query
        mock_production = Production(
            id=1,
            product_id=1,
            quantity_produced=100,
            date_produced=datetime(2024, 12, 10).date()
        )

        # Configure `all` method for the mock
        mock_query.all.return_value = [mock_production]

        # Mock the `to_dict` method for serialization
        mock_production.to_dict = lambda: {
            "id": mock_production.id,
            "product_id": mock_production.product_id,
            "quantity_produced": mock_production.quantity_produced,
            "date_produced": str(mock_production.date_produced)
        }

        # Debugging: Ensure mock is set
        print(f"Mock production to_dict: {mock_production.to_dict()}")

        # Expected response
        expected_response = [{
            "id": 1,
            "product_id": 1,
            "quantity_produced": 100,
            "date_produced": "2024-12-10"
        }]

        # Send GET request
        response = self.client.get('/api/productions', headers={"Authorization": "Bearer mock_token"})
        response_data = response.get_json()

        # Debugging output
        print(f"Mock called? {mock_query.all.called}")
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response_data}")

        # Assertions
        self.assertEqual(response.status_code, 200, f"Unexpected status code: {response.status_code}")
        self.assertEqual(response_data, expected_response, f"Unexpected response data: {response_data}")

        # Ensure the mock was called
        mock_query.all.assert_called_once()








    @patch('factory_management.models.db.session.add')
    @patch('factory_management.models.db.session.commit')
    def test_create_production(self, mock_commit, mock_add):
        """Test creating a new production record."""
        # Simulate POST request
        response = self.client.post('/api/productions', json={
            "product_id": 1,
            "quantity_produced": 100,
            "date_produced": "2024-12-10"
        }, headers={"Authorization": "Bearer mock_token"})
        print(f"Create production response status: {response.status_code}")
        response_data = response.get_json()
        print(f"Create production response data: {response_data}")

        # Assertions
        self.assertEqual(response.status_code, 201, f"Unexpected status code: {response.status_code}")
        self.assertEqual(response_data['message'], "Production record created successfully")

        # Ensure the mocks were called
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
