# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SSHconnect(models.Model):
    user = models.CharField(max_length=130)
    port = models.CharField(max_length=6)
    ip = models. GenericIPAddressField()
    status = models.CharField(max_length=10, null=True)


class BashScript(models.Model):
    author = models.CharField(max_length=130)
    name =  models.CharField(max_length=130)
    script = models.TextField()
    created = models.DateTimeField(auto_now_add=True)