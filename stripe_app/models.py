from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название элемента")
    description = models.TextField(blank=True, null=True, verbose_name="Описание элемента")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена элемента"
    )

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"
