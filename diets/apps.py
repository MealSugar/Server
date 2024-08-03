from django.apps import AppConfig
from django.conf import settings


class DietsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diets'
    
    def ready(self):
            if settings.SCHEDULER_DEFAULT:
                from . import operator
                operator.start()