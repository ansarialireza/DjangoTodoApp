import requests
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


class WeatherApiView(generics.GenericAPIView):
    api_key = 'c4c524d187e81608b563f148bc298d5d'

    def get(self,request,*args,**kwargs):
        city = request.Get.get('city','London')
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}units=metric'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            return Response (data,status = status.HTTP_200_OK)
        else:
            return Response({'error':data.get('message','Error fetching data')})