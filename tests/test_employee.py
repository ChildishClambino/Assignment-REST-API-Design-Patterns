import unittest
from unittest.mock import patch
from factory_management.factory import create_app
from factory_management.models import Employee

class TestEmployeeEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('factory_management.models.Employee.query.all')
    def test_get_employees(self, mock_query):
        mock_query.return_value = [
            Employee(id=1, name="John Doe", position="Manager"),
            Employee(id=2, name="Jane Doe", position="Developer")
        ]
        response = self.client.get('/api/employees')
        self.assertEqual(response.status_code, 200)
        self.assertIn("John Doe", response.get_data(as_text=True))

    @patch('factory_management.models.db.session.add')
    @patch('factory_management.models.db.session.commit')
    def test_create_employee(self, mock_commit, mock_add):
        response = self.client.post('/api/employees', json={"name": "Alice", "position": "Analyst"})
        self.assertEqual(response.status_code, 201)

    def test_get_employees_invalid_method(self):
        response = self.client.post('/api/employees')
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()
