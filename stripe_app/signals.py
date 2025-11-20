from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Discount, Tax, Order
from .services import create_stripe_coupon, create_stripe_tax


@receiver(post_save, sender=Discount)
def create_stripe_coupon_signal(sender, instance, created, **kwargs):
    """
    Сигнал для автоматического создания купона в Stripe при создании Discount.

    Срабатывает после сохранения модели Discount и создает соответствующий купон в Stripe,
    сохраняя его ID в поле stripe_coupon_id.
    """
    if created and not instance.stripe_coupon_id:
        coupon_id = create_stripe_coupon(instance)
        if coupon_id:
            Discount.objects.filter(id=instance.id).update(stripe_coupon_id=coupon_id)


@receiver(post_save, sender=Tax)
def create_stripe_tax_signal(sender, instance, created, **kwargs):
    """
    Сигнал для автоматического создания налоговой ставки в Stripe при создании Tax.

    Срабатывает после сохранения модели Tax и создает соответствующую налоговую ставку в Stripe,
    сохраняя ее ID в поле stripe_tax_id.
    """
    if created and not instance.stripe_tax_id:
        tax_id = create_stripe_tax(instance)
        if tax_id:
            Tax.objects.filter(id=instance.id).update(stripe_tax_id=tax_id)


@receiver(m2m_changed, sender=Order.items.through)
def update_order_total(sender, instance, action, **kwargs):
    """
    Сигнал для автоматического пересчета общей стоимости заказа при изменении состава товаров.

    Срабатывает при добавлении, удалении или очистке товаров в заказе и вызывает
    пересчет общей стоимости с учетом скидок и налогов.
    """
    if action in ["post_add", "post_remove", "post_clear"]:
        instance.calc_total_price()
