from django.urls import path
from .views import weather_list

app_name = 'core'

urlpatterns = [
    path('', weather_list, name='weather_list')
]
