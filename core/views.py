from django.shortcuts import render

def weather_list(request):
    return render(request, 'core/base.html')


