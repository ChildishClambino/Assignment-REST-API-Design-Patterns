import unittest
from unittest.mock import patch, MagicMock
from factory_management.factory import create_app

class TestEmployeeEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up the test client for Flask."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()  

    def tearDown(self):
        """Tear down the application context."""
        self.app_context.pop()

    @patch('factory_management.blueprints.employee.Employee.query')
    def test_get_employees(self, mock_query):
        """Test retrieving all employees."""
        mock_employee1 = MagicMock()
        mock_employee1.to_dict.return_value = {
            "id": 1,
            "name": "John Doe",
            "position": "Manager"
        }
        mock_employee2 = MagicMock()
        mock_employee2.to_dict.return_value = {
            "id": 2,
            "name": "Jane Smith",
            "position": "Developer"
        }

        mock_query.all.return_value = [mock_employee1, mock_employee2]

        # Debugging mock values
        print("Mock Employee 1:", mock_employee1.to_dict())
        print("Mock Employee 2:", mock_employee2.to_dict())

        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        print("Mocked response data:", response_data)  # Debugging
        self.assertEqual(len(response_data), 2)
        self.assertDictEqual(response_data[0], {"id": 1, "name": "John Doe", "position": "Manager"})
        self.assertDictEqual(response_data[1], {"id": 2, "name": "Jane Smith", "position": "Developer"})

    def test_get_employees_invalid_method(self):
        """Test accessing /api/employees with an invalid HTTP method."""
        response = self.client.post('/api/employees/')  
        self.assertEqual(response.status_code, 405)  
if __name__ == '__main__':
    unittest.main()
