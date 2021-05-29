from django.core.management.base import BaseCommand
from scraper import scraper


class Command(BaseCommand):
    help = "Queries the API and updates product data if possible"

    def handle(self, *args, **options):
        num_updated, num_products = scraper.scrape()

        style = self.style.SUCCESS
        if num_updated == 0:
            style = self.style.ERROR
        elif num_updated < num_products:
            style = self.style.WARNING

        self.stdout.write(style(f"{num_updated} of {num_products} products updated"))
