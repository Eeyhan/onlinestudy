from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class GenericConfig(AppConfig):
    name = 'generic'

    def ready(self):
        autodiscover_modules('startX')
