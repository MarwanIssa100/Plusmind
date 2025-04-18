from django.apps import AppConfig


class TherapistConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.therapist"

    def ready(self):
        import apps.therapist.signals
