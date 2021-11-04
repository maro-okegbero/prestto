from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', homepage, name='homepage'),
    path('sign_up', sign_up, name="register"),
    path('sign_in', sign_in, name="sign_in"),
    path('prestto_admin', admin_page, name="prestto_admin"),
    path('logout', admin_page, name="logout"),

]
