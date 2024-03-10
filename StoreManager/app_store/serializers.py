from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import GoodCategory, Provider, Good, Sale


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

class SaleSerializer(ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'