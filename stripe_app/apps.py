from django.apps import AppConfig


class StripeAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stripe_app"

    def ready(self):
        import stripe_app.signals
