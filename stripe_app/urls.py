from django.urls import path

from stripe_app.apps import StripeAppConfig
from stripe_app.views import (
    item_detail,
    create_checkout_session,
    order_detail,
    create_order_checkout_session,
)

app_name = StripeAppConfig.name

urlpatterns = [
    path("item/<int:item_id>/", item_detail, name="item_detail"),
    path("buy/<int:item_id>/", create_checkout_session, name="create_checkout_session"),
    path("order/<int:order_id>/", order_detail, name="order_detail"),
    path(
        "order_buy/<int:order_id>/",
        create_order_checkout_session,
        name="create_order_checkout_session",
    ),
]
