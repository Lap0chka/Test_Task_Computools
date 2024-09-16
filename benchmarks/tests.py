import json
import os
from datetime import datetime

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse


class BenchmarkResultsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set up the test data for all test cases.

        This method creates a temporary test file `test_database.json` containing
        benchmarking results used across all test cases. It loads two benchmarking
        results, which are later used to test the average calculation endpoints.
        """
        cls.test_data = {
            "benchmarking_results": [
                {
                    "request_id": "1",
                    "prompt_text": "Translate the following English text to French: 'Hello, how are you?'",
                    "generated_text": "Bonjour, comment ça va?",
                    "token_count": 5,
                    "time_to_first_token": 150,
                    "time_per_output_token": 30,
                    "total_generation_time": 300,
                    "timestamp": "2024-06-01T12:00:00"
                },
                {
                    "request_id": "2",
                    "prompt_text": "Summarize the following article: 'Artificial intelligence is transforming the world.'",
                    "generated_text": "AI is changing the world.",
                    "token_count": 6,
                    "time_to_first_token": 200,
                    "time_per_output_token": 25,
                    "total_generation_time": 350,
                    "timestamp": "2024-06-01T13:00:00"
                }
            ]
        }
        cls.test_file_path = settings.BASE_DIR / 'test_database.json'
        with open(cls.test_file_path, 'w') as f:
            json.dump(cls.test_data, f)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the test environment after all test cases have run.

        This method deletes the temporary `test_database.json` file that was created
        during `setUpTestData`. It ensures the test environment remains clean after
        all tests are finished.
        """
        cls.test_file_path.unlink()

    def setUp(self):
        """
        Set up the client instance for each test case.

        A new instance of the Django `Client` is created before each test to simulate
        HTTP requests to the application endpoints.
        """
        self.client = Client()

    def test_get_average_results(self):
        """
        Test the 'GET /results/average/' endpoint.

        This test verifies that the average statistics (e.g., token count, time to first
        token, time per output token, and total generation time) are calculated correctly
        across all available benchmarking results.
        """
        response = self.client.get(reverse('average-results'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['avg_token_count'], 5.5)
        self.assertEqual(data['avg_time_to_first_token'], 175)
        self.assertEqual(data['avg_time_per_output_token'], 27.5)
        self.assertEqual(data['avg_total_generation_time'], 325)

    def test_get_average_results_with_time(self):
        """
        Test the 'GET /results/average/{start_time}/{end_time}' endpoint.

        This test verifies that the average statistics are correctly calculated for
        benchmarking results within the specified time window. It uses a time window
        that includes only one result, so the averages should match the values of that
        single result.
        """
        start_time = "2024-06-01T12:00:00"
        end_time = "2024-06-01T12:59:59"
        url = reverse('average-results-with-time', args=[start_time, end_time])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['avg_token_count'], 5)
        self.assertEqual(data['avg_time_to_first_token'], 150)
        self.assertEqual(data['avg_time_per_output_token'], 30)
        self.assertEqual(data['avg_total_generation_time'], 300)

    def test_no_data_with_time_range(self):
        """
        Test the 'GET /results/average/{start_time}/{end_time}' endpoint with no results.

        This test verifies that when there are no benchmarking results within the given
        time window, the application returns an empty JSON response. The time window
        used here is outside of the range of any results in the test dataset.
        """
        start_time = "2023-01-01T00:00:00"
        end_time = "2023-12-31T23:59:59"
        url = reverse('average-results-with-time', args=[start_time, end_time])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, {})

