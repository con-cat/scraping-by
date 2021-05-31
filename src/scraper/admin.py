# Register your models here.
from django.contrib import admin

from . import scraper
from .models import Product


@admin.action(description="Scrape selected products")
def scrape(modeladmin, request, queryset):
    scraper.scrape(queryset)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [scrape]
    list_display = (
        "__str__",
        "current_price",
        "is_on_special",
        "savings_amount",
        "updated_at",
    )
