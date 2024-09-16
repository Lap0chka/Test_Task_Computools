import json
import os

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(DEBUG=True)
class BenchmarkResultsTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Set up the test data for all test cases.

        This method creates a temporary test file `test_database.json` containing
        benchmarking results used across all test cases. It loads two benchmarking
        results, which are later used to test the average calculation endpoints.
        """
        file_path = os.path.join(settings.BASE_DIR, 'test_database.json')
        with open(file_path, 'r') as file:
            cls.test_data = json.load(file)

        cls.test_file_path = settings.BASE_DIR / 'test_database_test.json'
        with open(cls.test_file_path, 'w') as f:
            json.dump(cls.test_data, f)

    def test_get_average_results(self):
        """
        Test the 'GET /results/average/' endpoint.

        This test verifies that the average statistics (e.g., token count, time to first
        token, time per output token, and total generation time)
        are calculated correctly
        across all available benchmarking results.
        """
        response = self.client.get(reverse('average-results'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['avg_token_count'], 10.2)
        self.assertEqual(data['avg_time_to_first_token'], 216.0)
        self.assertEqual(data['avg_time_per_output_token'], 27.6)
        self.assertEqual(data['avg_total_generation_time'], 485.2)

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
        Test the 'GET /results/average/{start_time}/{end_time}'
        endpoint with no results.

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
