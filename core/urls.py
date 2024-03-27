from django.urls import path
from .views import weather_list, forecast

app_name = 'core'

urlpatterns = [
    path('', weather_list, name='weather_list'),
    path('forecast/', forecast, name='forecast')
]
