import stripe
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from config.settings import STRIPE_API_KEY, STRIPE_PUBLIC_KEY
from stripe_app.models import Item

stripe.api_key = STRIPE_API_KEY


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(
        request,
        "stripe_app/item_detail.html",
        {"item": item, "STRIPE_PUBLIC_KEY": STRIPE_PUBLIC_KEY},
    )


def create_checkout_session(request, id):
    item = get_object_or_404(Item, id=id)

    try:
        product = stripe.Product.create(name=item.name)

        price = stripe.Price.create(
            currency="usd",
            unit_amount=int(item.price * 100),
            product=product.id,
        )

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price.id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(f"/stripe_app/item/{item.id}/"),
            cancel_url=request.build_absolute_uri(f"/stripe_app/item/{item.id}/"),
        )

        return JsonResponse({"sessionId": session.id})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
