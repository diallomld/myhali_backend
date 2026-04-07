import string
from django.core import serializers
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from api.models import Address
from api.serializers import *

# Create your views here.


@api_view(['GET'])
def isLocation_coded(request):
    try:
        location = request.GET.get('location')
        address = Address.objects.filter(location_name=location).last()
        generated_code = address.generated_code
        return Response({'isLocation_exists': True, "code": generated_code})
    except Address.DoesNotExist:
        return Response({'isLocation_exists': False})


@api_view(['POST'])
def save_code(request):
    data = JSONParser().parse(request)
    serializer = AddressSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def get_code(request):
    try:
        code = request.GET.get('code')
        address = Address.objects.get(generated_code=code)
        latitude = address.latitude
        longitude = address.longitude
        return Response({"latitude": latitude, "longitude": longitude})
    except Address.DoesNotExist:
        return Response({"latitude": None, "longitude": None})
