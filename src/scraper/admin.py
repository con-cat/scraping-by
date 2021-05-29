# Register your models here.
from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "current_price",
        "is_on_special",
        "savings_amount",
        "updated_at",
    )
