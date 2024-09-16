from django.urls import path

from . import views

urlpatterns = [
    path('results/average/', views.get_average_results, name='average-results'),
    path('results/average/<str:start_time>/<str:end_time>/',
         views.get_average_results_with_time, name='average-results-with-time'),
]
