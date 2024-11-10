from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
import requests
from .serializers import WeatherRequestSerializer  # Import the serializer

@method_decorator(cache_page(1200), name='dispatch')
class WeatherApiView(generics.GenericAPIView):
    api_key = 'c4c524d187e81608b563f148bc298d5d'
    serializer_class = WeatherRequestSerializer

    def get(self, request, *args, **kwargs):
        city = request.GET.get('city', 'London')
        return self.fetch_weather(city)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            city = serializer.validated_data['city']
            return self.fetch_weather(city)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def fetch_weather(self, city):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': data.get('message', 'Error fetching data')}, status=status.HTTP_400_BAD_REQUEST)
        

class WeatherView(TemplateView):
    template_name = 'weather/weather.html'