from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


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
        return lat, lon         # Returns the Latitiude and Longitude of the city 
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
    

def forecast(request):
    url = (f"https://api.openweathermap.org/data/2.5/forecast?lat=44.34&lon=10.99&appid"
           f"=98e201f7d727e4a86953ff2b72e265eb&units=metric")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast_data = get_forecast_weather(data)
    else:
        forecast_data = None
    context = {'forecast_data': forecast_data}
    return render(request, 'core/forecast.html', context=context)


def get_forecast_weather(data):
    forecast_data = []
    weather_data = []
    for i in range(len(data['list'])):
        time = data["list"][i]['dt_txt'].split(' ')
        if '12:00:00' in time:
            weather_data.append(data['list'][i])
    for data in weather_data:
        pass    
