from datetime import datetime

from django.http import HttpResponse, JsonResponse

from .utils import load_benchmarking_results


def calculate_average(results):
    """
    Calculate average statistics from a list of benchmarking results.

    This function computes the average values for various performance metrics
    from a given list of benchmarking results, including token count, time
    to first token, time per output token, and total generation time.

    """
    total_results = len(results)
    if total_results == 0:
        return {}

    total_token_count = 0
    total_time_to_first_token = 0
    total_time_per_output_token = 0
    total_generation_time = 0

    for r in results:
        total_token_count += r.get('token_count', 0)
        total_time_to_first_token += r.get('time_to_first_token', 0)
        total_time_per_output_token += r.get('time_per_output_token', 0)
        total_generation_time += r.get('total_generation_time', 0)

    avg_stats = {
        'avg_token_count': total_token_count / total_results,
        'avg_time_to_first_token': total_time_to_first_token / total_results,
        'avg_time_per_output_token': total_time_per_output_token / total_results,
        'avg_total_generation_time': total_generation_time / total_results,
    }

    return avg_stats


def get_average_results(request):
    """
    Retrieve average performance statistics from benchmarking results.

    This view function handles an HTTP GET request to calculate and return
    the average statistics for various performance metrics from the
    benchmarking results. It loads the benchmarking results from a data
    source and computes the averages using the `calculate_average` function.
    """
    results = load_benchmarking_results()
    avg_stats = calculate_average(results)
    return JsonResponse(avg_stats)


def get_average_results_with_time(request, start_time, end_time):
    """
    Retrieve average performance statistics for benchmarking
    results within a specified time range.

    This view function handles an HTTP GET request to calculate and return
    the average statistics for various performance metrics from the
    benchmarking results filtered by a specified time range. It loads the
    benchmarking results from a data source and computes the averages using
    the `calculate_average` function.

    """
    results = load_benchmarking_results()

    # Convert the string timestamps to datetime objects
    try:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
    except ValueError:
        return HttpResponse('Time format should be YYYY-MM-DDTHH:MM:SS')

    # Filter results by timestamp range
    filtered_results = [r for r in results
                        if start_dt <= datetime.fromisoformat(r['timestamp']) <= end_dt]

    avg_stats = calculate_average(filtered_results)
    return JsonResponse(avg_stats)
