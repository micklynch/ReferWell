import unittest
from unittest.mock import patch
from src.utils.patient_demographics import get_patient_demographics

# FILE: src/utils/test_patient_demographics.py


class TestGetPatientDemographics(unittest.TestCase):

    @patch('src.utils.patient_demographics.requests.get')
    def test_get_patient_demographics(self, mock_get):
        # Mock response data
        mock_response = {
            "name": [{"given": ["John"], "family": "Doe"}],
            "address": [{"line": ["123 Main St"], "city": "Anytown", "state": "CA", "postalCode": "12345"}]
        }
        mock_get.return_value.json.return_value = mock_response

        # Expected result
        expected_result = {
            "name": "John Doe",
            "address": "123 Main St, Anytown, CA 12345"
        }

        # Call the function
        result = get_patient_demographics("46085643")

        # Assert the result
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()