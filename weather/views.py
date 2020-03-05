import requests

from .models import City
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CityForm

from .settings import api_key


def index(request):
    cities = City.objects.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=Metric&appid={}'

    all_cities = []
    for city in cities:
        r = requests.get(url.format(city.name, api_key)).json()
        if r['cod'] == 200:
            city_info = {
                'city': city.name,
                'temp': round(r['main']['temp']),
                'icon': r['weather'][0]['icon'],
                'humidity': r['main']['humidity'],
                'pressure': r['main']['pressure'],
                'wind_speed': r['wind']['speed'],
            }
            all_cities.append(city_info)

    if request.method == 'POST':
        form = CityForm(request.POST)
        try:
            r = requests.get(url.format(form.data['name'], api_key))
            if r.status_code == 200:
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Информация успешно добавлена.')
                return redirect('index.html')
            else:
                messages.add_message(request, messages.ERROR, 'Такого города не существует.')
        except ValueError:
            messages.add_message(request, messages.ERROR, 'Такой город уже присутствует в списке.')

    form = CityForm()
    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather/index.html', context=context)
