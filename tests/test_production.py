import unittest
from unittest.mock import patch
from factory_management.factory import create_app
from factory_management.models import Production

class TestProductionEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('factory_management.models.Production.query.all')
    def test_get_productions(self, mock_query):
        mock_query.return_value = [
            Production(id=1, product_id=1, quantity_produced=100, date_produced="2024-12-10")
        ]
        response = self.client.get('/api/productions')
        self.assertEqual(response.status_code, 200)
        self.assertIn("100", response.get_data(as_text=True))

    @patch('factory_management.models.db.session.add')
    @patch('factory_management.models.db.session.commit')
    def test_create_production(self, mock_commit, mock_add):
        response = self.client.post('/api/productions', json={
            "product_id": 1,
            "quantity_produced": 100,
            "date_produced": "2024-12-10"
        })
        self.assertEqual(response.status_code, 201)

    def test_get_productions_invalid_method(self):
        response = self.client.post('/api/productions')
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()
