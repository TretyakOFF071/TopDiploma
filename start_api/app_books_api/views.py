from django.shortcuts import render
from .serializers import *
from .models import Author, Book
from rest_framework.views import APIView
from django.http import JsonResponse


class AuthorListAPIView(APIView):

    def get(self, request):
        queryset = Author.objects.all()
        return JsonResponse(AuthorSerializer(queryset, many=True).data, safe=False)



