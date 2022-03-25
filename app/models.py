# -*- encoding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import os
from core.settings import MEDIA_URL



# Create your models here.

class SSHconnect(models.Model):
    user = models.CharField(max_length=130)
    port = models.CharField(max_length=6)
    ip = models. GenericIPAddressField()
    status = models.CharField(max_length=10, null=True)
    vnc_installed = models.BooleanField(default=False)


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class BashScript(models.Model):
    author = models.CharField(max_length=130)
    name =  models.CharField(max_length=130)
    point = models.CharField(max_length=4,blank=True)
    script = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=BashScript)
def create_user_profile(sender,instance, created, **kwargs):
    if created:
        print(instance.name)
        ScriptLevel.objects.create(name=instance.name)

@receiver(post_save, sender=BashScript)
def bash_script_save(sender, instance, created, **kwargs):
    if created:
        words= instance.script
        file = open(os.path.join(MEDIA_URL, '{}'.format(instance.name)), 'w')
        file.write(words)
        file.close()


# @receiver(post_save, sender=BashScript)
# def save_user_profile(sender,instance, **kwargs):
#     instance.scriptlevel.save()


class ScriptLevel(models.Model):
    name = models.CharField(max_length=130)
    point = models.CharField(max_length=3,blank=True)

class WordsPoint(models.Model):
    word = models.CharField(max_length=130)
    point = models.CharField(max_length=1)

