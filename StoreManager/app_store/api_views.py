from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache

from .models import Provider, Good
from .serializers import ProviderSerializer, GoodSerializer


CACHE_TIME = 60 * 60 * 2

class ProviderAPIView(APIView):

    def get(self, request):
        data = cache.get_or_set('providers_list', Provider.objects.all(), CACHE_TIME)
        return JsonResponse(ProviderSerializer(data, many=True).data, safe=False)

    def post(self, request):
        serializer = ProviderSerializer(data=request.data)
        if serializer.is_valid():
            cache.delete('providers_list')
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProviderDetailAPI(APIView):

    def get(self, request, pk):
        provider = get_object_or_404(Provider, pk=pk)
        data = cache.get_or_set(f'provider_{pk}', provider, CACHE_TIME)
        return JsonResponse(ProviderSerializer(data).data, safe=False)

    def put(self, request, pk):
        provider = get_object_or_404(Provider, pk=pk)
        serializer = ProviderSerializer(provider, data=request.data)
        if serializer.is_valid():
            cache.delete(f'provider_{pk}')
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoodAPIView(APIView):

    def get(self, request):
        data = cache.get_or_set('goods_list', Good.objects.all(), CACHE_TIME)
        return JsonResponse(GoodSerializer(data, many=True).data, safe=False)

    def post(self, request):
        serializer = GoodSerializer(data=request.data)
        if serializer.is_valid():
            cache.delete('goods_list')
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodDetailAPI(APIView):

    def get(self, request, pk):
        good = get_object_or_404(Good, pk=pk)
        data = cache.get_or_set(f'good_{pk}', good, CACHE_TIME)
        return JsonResponse(GoodSerializer(data).data, safe=False)

    def put(self, request, pk):
        good = get_object_or_404(Good, pk=pk)
        serializer = GoodSerializer(good, data=request.data)
        if serializer.is_valid():
            cache.delete(f'good_{pk}')
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)