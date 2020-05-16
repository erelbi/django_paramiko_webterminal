# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf.urls import url
from django.urls import path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView
from app.register import clientregister,send_command

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),


]
