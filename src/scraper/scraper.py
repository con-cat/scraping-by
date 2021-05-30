import logging
import typing as t

import requests
from django.conf import settings

from . import models


class ErrorFetchingProduct(Exception):
    pass


def get_product_data(product_id: int) -> t.Dict:
    try:
        response = requests.get(settings.API_URL.format(str(product_id)), timeout=5)
        response.raise_for_status()
        return response.json()["Product"]
    except Exception as e:
        raise ErrorFetchingProduct(str(e))


def scrape() -> t.Tuple[int, int]:
    updated_count = 0
    products = models.Product.objects.all()
    for product in products:
        # Try to get the product's data from the API
        try:
            product_data = get_product_data(product.ww_id)
        except ErrorFetchingProduct as err:
            logging.warning(f"Error fetching product {product}: {err}")
            continue

        product.update_data_from_api(
            name=product_data["Name"].strip(),
            current_price=product_data["InstorePrice"],
            is_on_special=product_data["InstoreIsOnSpecial"],
            previous_price=product_data["InstoreWasPrice"],
            savings_amount=product_data["InstoreSavingsAmount"],
        )
        updated_count += 1

    return updated_count, len(products)
