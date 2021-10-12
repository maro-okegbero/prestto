from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', homepage),
    path('sign_up', sign_up),
    path('sign_in', sign_in),
]
