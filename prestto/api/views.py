from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from prestto.api.serializers import UserSerializer, LoginSerializer, BusinessNameSerializer


@csrf_exempt
@api_view(['POST'])
def register_user(request):
    """
    Register a user
    """
    # data = JSONParser().parse(request.data)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            token = user.token
            json = serializer.data
            json['token'] = token
            return Response(json, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Log a user in using the username and password as the authentication credentials
    """
    data = request.data
    print(data, "User===========")
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_business_name(request):
    """

    :param request:
    :return:
    """
    data = request.data
    serializer = BusinessNameSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        message = {"status": "success"}
        return Response(message, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








