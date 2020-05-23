# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import os
from core.settings import MEDIA_URL
import collections
# from  .script_level_calculator import calculator

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

@receiver(post_save, sender=BashScript)
def create_user_profile(sender,instance, created, **kwargs):
    if created:
        print(instance.name)
        ScriptLevel.objects.create(name=instance.name)

@receiver(post_save, sender=BashScript)
def bash_script_save(sender, instance, created, **kwargs):
    if created:
        print("model içerde")
        words= instance.script
        file = open(os.path.join(MEDIA_URL, '{}'.format(instance.name)), 'w')
        file.write(words)
        script_in_word = WordsPoint.objects.values_list('word', flat=True)
        words_split = words.split()
        word_counts = collections.Counter(words_split)
        for word, count in sorted(word_counts.items()):
            if str(word) in script_in_word:
                p = WordsPoint.objects.filter(word=word).values('point').first()
                total = (int(p['point'])*int(count))
                ScriptLevel.objects.filter(name=instance.name).update(point= int(total))
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

