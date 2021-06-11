from django.shortcuts import render

from django.contrib.auth.models import User, Group
from django.http import HttpResponse, FileResponse, HttpResponseBadRequest, JsonResponse
from rest_framework import viewsets, permissions, views, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from .serializers import UserSerializer, GroupSerializer
from .models import Mahasiswa
from rest_framework.views import exception_handler
import zipfile
import zlib
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

@api_view(['POST'])
def update_data(request):
    json_data = json.loads(request.body.decode('utf8'))
    npm = json_data["npm"]
    nama = json_data["nama"]
    mhs_obj = Mahasiswa.objects.filter(npm=npm)
    print(json.loads(request.body.decode('utf8')))
    if mhs_obj:
        return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "error": "Data with npm " + npm + " already exists",
                },
            )
    else:
        new_mhs_obj = Mahasiswa(npm=npm, nama=nama)
        new_mhs_obj.save()
    return Response(
        status = status.HTTP_201_CREATED,
        data = {
            "message" : "Data Updated Successfully"
        }
    )

@api_view(['GET'])
def retrieve_data(request, npm=None):

    mhs_obj = Mahasiswa.objects.filter(npm=npm)
    if not mhs_obj:
        return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "error": "Data with npm " + npm + " doesn't exists",
                },
            )
    print(mhs_obj.get().npm)
    print(mhs_obj.get().nama)
    data = {
            "status" : "OK",
            "npm" : mhs_obj.get().npm,
            "nama" : mhs_obj.get().nama 
        }
    return JsonResponse(data, safe=False)

