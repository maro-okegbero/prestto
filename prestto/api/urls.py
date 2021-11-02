from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('register', register_user, name='register'),
    path('login', register_user, name='login'),
    path('business_name', register_business_name, name='business_name'),
]
