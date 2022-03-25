# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views
from app.register import clientregister
from app.web_terminal import send_command,client_script_operation
from app.register.ajax_request import ajax_delete, ajax_update
from app.clientInfo import InfoPage
urlpatterns = [
    # Matches any html file 
    re_path(r'^.*\.html', views.pages, name='pages'),
    #
    # # The home page
    path('', views.index, name='home'),
    re_path(r'^clientregister/$', clientregister.Register.as_view(), name="registerFTP"),
    re_path(r'^(?P<ip>[0-9_.]+)/client_page$', InfoPage.Infoclient.as_view(), name="client_page"),
    re_path(r'^(?P<ip>[0-9_.]+)/send_command$', send_command.SSHclient.as_view(), name="client_command"),
    re_path(r'^(?P<ip>[0-9_.]+)/client_log$', send_command.SSHclient.as_view(), name="client_log"),
    re_path(r'^(?P<ip>[0-9_.]+)/script_delete$', client_script_operation.script, name="script_delete"),
    re_path(r'^(?P<ip>[0-9_.]+)/client_info', InfoPage.Infoclient.client_info, name="client_info"),
    re_path(r'^(?P<ip>[0-9_.]+)/send_command/(?P<command>[^\n]+)/$', send_command.SSHclient.stream, name="result"),
    re_path(r'^(?P<ip>[0-9_.]+)/delete/$', ajax_delete, name="delete"),
    re_path(r'^(?P<ip>[0-9_.]+)/update/$', ajax_update, name="update"),

]
