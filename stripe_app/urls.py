from django.urls import path

from stripe_app.apps import StripeAppConfig
from stripe_app.views import (
    item_detail,
    create_checkout_session,
    order_detail,
    create_order_checkout_session,
    payment_intent_page,
    create_payment_intent,
    create_order_payment_intent,
    order_payment_intent_page,
)

app_name = StripeAppConfig.name

urlpatterns = [
    # session
    path("item/<int:item_id>/", item_detail, name="item_detail"),
    path("buy/<int:item_id>/", create_checkout_session, name="create_checkout_session"),
    path("order/<int:order_id>/", order_detail, name="order_detail"),
    path(
        "order_buy/<int:order_id>/",
        create_order_checkout_session,
        name="create_order_checkout_session",
    ),
    # payment intent
    path(
        "payment-intent/<int:item_id>/", payment_intent_page, name="payment_intent_page"
    ),
    path(
        "create-payment-intent/<int:item_id>/",
        create_payment_intent,
        name="create_payment_intent",
    ),
    path(
        "order-payment-intent/<int:order_id>/",
        order_payment_intent_page,
        name="order_payment_intent_page",
    ),
    path(
        "create-order-payment-intent/<int:order_id>/",
        create_order_payment_intent,
        name="create_order_payment_intent",
    ),
]
