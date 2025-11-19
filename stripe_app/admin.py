from django.contrib import admin

from stripe_app.models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    search_fields = ["name"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "total_price"]
    filter_horizontal = ["items"]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ["name", "percent", "stripe_coupon_id"]


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ["name", "percent", "stripe_tax_id"]
