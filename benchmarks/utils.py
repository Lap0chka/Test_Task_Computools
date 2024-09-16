import json
import os

from django.conf import settings
from django.http import HttpResponse


def load_benchmarking_results():
    """
    Load benchmarking results from a JSON file.

    This function reads benchmarking results from a predefined JSON file
    located in the project's base directory. It returns the results as a
    list of dictionaries, where each dictionary contains the details of a
    benchmarking result.
    """
    if not settings.DEBUG:
        raise Exception("Feature not ready for live environment.")

    file_path = os.path.join(settings.BASE_DIR, 'test_database.json')
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data['benchmarking_results']
    except FileNotFoundError:
        return HttpResponse('The program cant\'t find the file\n '
                            'You should put file of the top')
