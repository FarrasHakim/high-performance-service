from django.shortcuts import render

from django.contrib.auth.models import User, Group
from django.http import HttpResponse, FileResponse, HttpResponseBadRequest, JsonResponse
from rest_framework import viewsets, permissions, views, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from .serializers import UserSerializer, GroupSerializer
from rest_framework.views import exception_handler
import zipfile
import zlib
import requests
import json

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
def read_data(request, id=None):
    url = "http://localhost:8000/%s/" % id

    r = requests.get(url = url)
    data = r.json()
    print(data)
    return JsonResponse(data)

@api_view(['GET'])
def read_data_exist(request, id=None, trx_id=None):
    url = "http://localhost:8000/%s/" % id

    r = requests.get(url = url)
    data = r.json()
    print(data)
    return JsonResponse(data)



