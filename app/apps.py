from django.apps import AppConfig


class NotifierConfig(AppConfig):
    name = 'app'

    def ready(self):
        from . import signals