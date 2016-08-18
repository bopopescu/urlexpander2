from rest_framework import serializers
from .models import Url

class UrlDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Url
        fields = '__all__'

class UrlListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Url
        fields = ('id','shortened')