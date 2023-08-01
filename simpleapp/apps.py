from django.apps import AppConfig


class SimpleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simpleapp'

    def ready(self):
        from .signals import send_notifications, notify_about_new_post


