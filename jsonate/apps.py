from django.apps import AppConfig

class JsonateAppConfig(AppConfig):
    name = 'jsonate'

    def ready(self):
        # from . import monkey_patches
        pass