from django.apps import AppConfig


class SosiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SoSi'

def ready(self):
        # optionally import signals here later (e.g., to auto-create profiles)
        pass
