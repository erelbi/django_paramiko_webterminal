# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf.urls import url
from django.urls import path, re_path
from app import views
from app.register import clientregister, send_command

urlpatterns = [
    # Matches any html file 
    re_path(r'^.*\.html', views.pages, name='pages'),
    #
    # # The home page
    path('', views.index, name='home'),
    url(r'^clientregister/$', clientregister.Register.as_view(), name="registerFTP"),
    url(r'^clientregister/(?P<ip>[0-9_.]+)/$', send_command.SSHclient.as_view(), name="client_command"),
   url(r'^(?P<ip>[0-9_.]+)/$', send_command.post_ajax, name="ajax_send"),
    url(r'^clientregister/(?P<ip>[0-9_.]+)/(?P<command>[^\n]+)/$', send_command.SSHclient.stream,
        name="result"),
]
