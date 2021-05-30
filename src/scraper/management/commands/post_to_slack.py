from datetime import datetime, timedelta, timezone

from django.core.management.base import BaseCommand
from scraper import operations
from scraper.models import Product


class Command(BaseCommand):
    help = "Posts a Slack message with products currently on special"

    def handle(self, *args, **options):
        # Post products on special
        products_on_special = Product.objects.filter(
            is_on_special=True,
            updated_at__gte=datetime.now(timezone.utc) - timedelta(hours=24),
        )

        messages = [
            (
                f"🚨🤑 {product.name} is on special!!! "
                f"Current price is ${product.current_price}, "
                f"a {product.discount:.0%} discount!"
            )
            for product in products_on_special
        ]

        if messages:
            operations.post_message_to_slack("\n".join(messages))
            self.stdout.write("\n".join(messages))
        else:
            self.stdout.write(self.style.NOTICE("No specials today"))

        # Warn about products that haven't been updated for a while
        stale_products = Product.objects.filter(
            updated_at__lte=datetime.now(timezone.utc) - timedelta(days=5)
        )

        messages = [
            (
                f"🤔 {product.name} hasn't been updated for a while - "
                f"it was last successfully scraped on {product.updated_at}"
            )
            for product in stale_products
        ]

        if messages:
            operations.post_message_to_slack("\n".join(messages))
            self.stdout.write(self.style.WARNING("\n".join(messages)))
