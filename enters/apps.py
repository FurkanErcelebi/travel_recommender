from django.apps import AppConfig


class EntersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'enters'
    # def ready(self):
    #         from . import scheduler
    #         scheduler.start()
