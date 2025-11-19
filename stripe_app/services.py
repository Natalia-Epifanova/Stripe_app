import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_price_for_item(item):
    """
    Создает продукт и цену в Stripe для Item
    Возвращает price_id
    """
    try:
        product = stripe.Product.create(name=item.name)

        price = stripe.Price.create(
            currency=item.currency,
            unit_amount=int(item.price * 100),
            product=product.id,
        )
        return price.id
    except Exception as e:
        print(f"Ошибка при создании цены в stripe для {item.name}: {e}")
        return None


def create_stripe_coupon(discount_instance):
    """Создает купон в Stripe для модели Discount"""
    try:
        coupon = stripe.Coupon.create(
            duration="forever",
            percent_off=float(discount_instance.percent),
            name=discount_instance.name,
        )
        return coupon.id
    except Exception as e:
        print(f"Ошибка при создании в stripe купона: {e}")
        return None


def create_stripe_tax(tax_instance):
    """Создает tax rate в Stripe для модели Tax"""
    try:
        tax_rate = stripe.TaxRate.create(
            display_name=tax_instance.name,
            percentage=float(tax_instance.percent),
            inclusive=True,
        )
        return tax_rate.id
    except Exception as e:
        print(f"Ошибка при создании в stripe налога: {e}")
        return None
