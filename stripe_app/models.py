from decimal import Decimal

from django.db import models


class Item(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название элемента",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание элемента",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена элемента",
    )
    currency = models.CharField(
        max_length=3,
        choices=[("usd", "USD"), ("eur", "EUR")],
        default="usd",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"


class Order(models.Model):
    items = models.ManyToManyField(Item, verbose_name="Элементы в заказе")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Общая цена элементов",
    )
    discount = models.ForeignKey(
        "Discount",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Скидка",
    )
    tax = models.ForeignKey(
        "Tax",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Налог",
    )

    @property
    def currency(self):
        return "usd"

    def calc_total_price(self):
        total = 0
        for item in self.items.all():
            if item.currency == "usd":
                total += item.price
            elif item.currency == "eur":
                total += item.price * Decimal("1.08")
        if self.discount:
            total -= total * self.discount.percent / 100
        if self.tax:
            total += total * self.tax.percent / 100
        self.total_price = total
        self.save()
        return total

    def __str__(self):
        return f"Order #{self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Discount(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название скидки/купона",
    )
    percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Процент скидки/купона",
    )
    stripe_coupon_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="ID купона для stripe",
    )

    def __str__(self):
        return f"{self.name} ({self.percent}%)"

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"


class Tax(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название налога",
    )
    percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Налоговая ставка",
    )
    stripe_tax_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="ID налога для stripe",
    )

    def __str__(self):
        return f"{self.name} ({self.percent}%)"

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"
