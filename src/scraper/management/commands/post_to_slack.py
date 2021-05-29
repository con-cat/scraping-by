from datetime import datetime, timedelta, timezone

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from scraper.models import Product


class Command(BaseCommand):
    help = "Posts a Slack message with products currently on special"

    def handle(self, *args, **options):
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
            if settings.SLACK_URL is not None:
                requests.post(
                    settings.SLACK_URL,
                    json={"text": "\n".join(messages)},
                )
            self.stdout.write("\n".join(messages))
        else:
            self.stdout.write(self.style.NOTICE("No specials today"))
