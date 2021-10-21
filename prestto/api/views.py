from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from prestto.api.serializers import UserSerializer


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

