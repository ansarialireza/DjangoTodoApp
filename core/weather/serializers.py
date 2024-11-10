# serializers.py
from rest_framework import serializers

class WeatherRequestSerializer(serializers.Serializer):
    city = serializers.CharField(required=True)