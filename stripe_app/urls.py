from django.urls import path

from stripe_app.apps import StripeAppConfig
from stripe_app.views import item_detail, create_checkout_session

app_name = StripeAppConfig.name

urlpatterns = [
    path("item/<int:id>/", item_detail, name="item_detail"),
    path("buy/<int:id>/", create_checkout_session, name="create_checkout_session"),
]
