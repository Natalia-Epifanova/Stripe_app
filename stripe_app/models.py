from decimal import Decimal

from django.db import models


class Item(models.Model):
    """
    Модель товара с информацией о названии, описании, цене и валюте.

    Attributes:
        name (str): Название товара
        description (str): Описание товара (опционально)
        price (Decimal): Цена товара
        currency (str): Валюта товара (USD или EUR)
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Название товара",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание товара",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена товара",
    )
    currency = models.CharField(
        max_length=3,
        choices=[("usd", "USD"), ("eur", "EUR")],
        default="usd",
        verbose_name="Валюта",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Discount(models.Model):
    """
    Модель скидки/купона для применения к заказам.

    Attributes:
        name (str): Название скидки
        percent (Decimal): Процент скидки
        stripe_coupon_id (str): ID купона в Stripe (создается автоматически)
    """

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
    """
    Модель налога для применения к заказам.

    Attributes:
        name (str): Название налога
        percent (Decimal): Процент налога
        stripe_tax_id (str): ID налога в Stripe (создается автоматически)
    """

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


class Order(models.Model):
    """
    Модель заказа, объединяющая несколько товаров с возможностью применения скидок и налогов.

    Attributes:
        items (ManyToManyField): Товары в заказе
        total_price (Decimal): Общая стоимость заказа после применения скидок и налогов
        discount (ForeignKey): Примененная скидка (опционально)
        tax (ForeignKey): Примененный налог (опционально)
    """

    items = models.ManyToManyField(Item, verbose_name="Товары в заказе")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Общая стоимость заказа",
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
        """
        Определяет валюту заказа на основе товаров.

        Returns:
            str: Код валюты заказа
        """
        if self.items.exists():
            return self.items.first().currency
        return "usd"

    def clean(self):
        """
        Валидация заказа - проверяет что все товары в одной валюте.
        """
        if self.pk and self.items.exists():
            currencies = set(item.currency for item in self.items.all())
            if len(currencies) > 1:
                from django.core.exceptions import ValidationError

                raise ValidationError(
                    f"Все товары в заказе должны быть в одной валюте. "
                    f"Обнаружены валюты: {', '.join(currencies)}"
                )

    def save(self, *args, **kwargs):
        """Переопределяем save для вызова валидации."""
        self.clean()
        super().save(*args, **kwargs)

    def calc_total_price(self):
        """
        Рассчитывает общую стоимость заказа с учетом скидок и налогов.

        Returns:
            Decimal: Общая стоимость заказа после всех расчетов
        """
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
