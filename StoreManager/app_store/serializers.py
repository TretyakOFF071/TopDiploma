from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import GoodCategory, Provider, Good


class ProviderSerializer(ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'


class GoodCategorySerializer(ModelSerializer):
    class Meta:
        model = GoodCategory
        fields = '__all__'


class GoodSerializer(ModelSerializer):
    class Meta:
        model = Good
        fields = '__all__'