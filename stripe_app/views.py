import stripe
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from config.settings import STRIPE_API_KEY, STRIPE_PUBLIC_KEY
from stripe_app.models import Item, Order
from stripe_app.services import create_stripe_price_for_item

stripe.api_key = STRIPE_API_KEY


def item_detail(request, item_id):
    """Страница элемента"""
    item = get_object_or_404(Item, id=item_id)
    return render(
        request,
        "stripe_app/item_detail.html",
        {"item": item, "STRIPE_PUBLIC_KEY": STRIPE_PUBLIC_KEY},
    )


def create_checkout_session(request, item_id):
    """Создание сессии для одного товара"""
    item = get_object_or_404(Item, id=item_id)

    try:
        price_id = create_stripe_price_for_item(item)

        if not price_id:
            return JsonResponse({"error": "Ошибка при создании цены"}, status=400)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
            success_url=request.build_absolute_uri(f"/stripe_app/item/{item.id}/"),
            cancel_url=request.build_absolute_uri(f"/stripe_app/item/{item.id}/"),
        )

        return JsonResponse({"sessionId": session.id})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def order_detail(request, order_id):
    """Страница заказа"""
    order = get_object_or_404(Order, id=order_id)
    order.calc_total_price()
    return render(
        request,
        "stripe_app/order_detail.html",
        {"order": order, "STRIPE_PUBLIC_KEY": STRIPE_PUBLIC_KEY},
    )


def create_order_checkout_session(request, order_id):
    """Создание сессии для товаров из заказа"""
    order = get_object_or_404(Order, id=order_id)
    order.calc_total_price()

    try:
        line_items = []
        tax_rates = []
        discounts = []

        if order.tax and order.tax.stripe_tax_id:
            tax_rates = [order.tax.stripe_tax_id]

        for item in order.items.all():
            price_id = create_stripe_price_for_item(item)
            if price_id:
                line_items.append(
                    {
                        "price": price_id,
                        "quantity": 1,
                        "tax_rates": tax_rates,
                    }
                )

        if not line_items:
            return JsonResponse({"error": "Отсутствуют элементы в заказе"}, status=400)

        if order.discount and order.discount.stripe_coupon_id:
            discounts.append({"coupon": order.discount.stripe_coupon_id})

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            discounts=discounts,
            mode="payment",
            success_url=request.build_absolute_uri(f"/stripe_app/order/{order.id}/"),
            cancel_url=request.build_absolute_uri(f"/stripe_app/order/{order.id}/"),
        )

        return JsonResponse({"sessionId": session.id})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
