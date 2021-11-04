from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', homepage, name='homepage'),
    path('sign_up', sign_up, name="register"),
    path('prestto_admin', admin_page, name="prestto_admin"),
    path('prestto_admin/business_name/<pk>', business_name_detail, name="bn_detail"),
    path('prestto_admin/ltd_rerquests', ltd_requests, name="ltd"),
    path('logout', sign_out, name="logout"),
    path('login', sign_in, name="login"),

]
