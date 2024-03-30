from django.shortcuts import render, get_object_or_404
import requests
from .models import City
from .forms import CityForm
from datetime import datetime


def weather_list(request):
    cities = City.objects.all()

    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            form.save()
            form = CityForm()
    else:
        form = CityForm()

    weather_data = []
    for city in cities:
        data = get_current_weather(city.name, city.country)
        city_weather = {
            "city_id": city.id,
            'name': data['name'],
            'main': data['weather'][0]['main'],
            'desc': data['weather'][0]['main'],
            'icon': data['weather'][0]['icon'],
            'main_temp': data['main']['temp'],
            'max_temp': data['main']['temp_min'],
            'min_temp': data['main']['temp_min'],
            'visiblity': data['visibility'],
            'wind_speed': data['wind']['speed'],
            'humidity': data['main']['humidity']
        }
        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'core/list.html', context=context)


# Get the latitude of a city in a partuclar country 
def _get_lat_lon(city, country):
    url = (f'https://api.openweathermap.org/geo/1.0/direct?q={city},{country}&limit=1&appid'
           f'=98e201f7d727e4a86953ff2b72e265eb')
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        lat = data[0]['lat']
        lon = data[0]['lon']
        return lat, lon  # Returns the Latitude and Longitude of the city
    else:
        return False


# Get the weather of the city based on the Latitude and Longitude of the city
def get_current_weather(city, country):
    if _get_lat_lon(city, country):
        lat, lon = _get_lat_lon(city, country)
        url = (f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid'
               f'=98e201f7d727e4a86953ff2b72e265eb&units=metric')
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
    else:
        print("Cant fetch data")


def forecast(request, id):
    city = get_object_or_404(City, id=id)
    lat, lon = _get_lat_lon(city.name, city.country)
    url = (f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid"
           f"=98e201f7d727e4a86953ff2b72e265eb&units=metric")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        country = data['city']['country']
        city = data['city']['name']
        forecast_data = get_forecast_weather(data)
    else:
        forecast_data = None
        country = None
        city = None
    context = {'forecast_data': forecast_data,
               'country': country,
               'city': city}
    return render(request, 'core/forecast.html', context=context)


def get_forecast_weather(data):
    weather_data = []
    for i in range(len(data['list'])):
        time = data["list"][i]['dt_txt'].split(' ')
        if '12:00:00' in time:
            weather_data.append(data['list'][i])
    forecast_data = _extract_forecast_data(weather_data)
    return forecast_data


def _extract_forecast_data(weather_data):
    forecast_data = []
    for weather in weather_data:
        date_str = weather['dt_txt'].split(' ')
        date_str = date_str[0]
        date_strp = datetime.strptime(date_str, '%Y-%m-%d')
        formated_date = date_strp.strftime('%A,%B %d %Y').split(',')
        day = formated_date[0]
        month = formated_date[1]
        day_weather = {
            'temp': weather['main']['temp'],
            'max_temp': weather['main']['temp_max'],
            'min_temp': weather['main']['temp_min'],
            'wind_speed': weather['wind']['speed'],
            'pressure': weather['main']['pressure'],
            'icon': weather['weather'][0]['icon'],
            'description': weather['weather'][0]['description'],
            'humidity': weather['main']['humidity'],
            'day': day,
            'month': month
        }
        forecast_data.append(day_weather)
    return forecast_data
