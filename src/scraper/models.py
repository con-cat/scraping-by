from datetime import datetime, timezone
from decimal import Decimal

from django.db import models


class Product(models.Model):
    # The supermarket's product ID
    ww_id = models.PositiveIntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=128, blank=True, default="")
    # InstorePrice from the API
    current_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    # InstoreIsOnSpecial
    is_on_special = models.BooleanField(default=False)
    # InstoreWasPrice and InstoreSavingsAmount
    previous_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    savings_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        if self.name:
            return f"{self.ww_id}: {self.name}"
        return str(self.ww_id)

    @property
    def discount(self) -> Decimal:
        if self.previous_price and self.savings_amount:
            return self.savings_amount / self.previous_price
        else:
            return Decimal(0)

    def update_data(
        self,
        *,
        name: str,
        current_price: Decimal,
        is_on_special: bool,
        previous_price: Decimal,
        savings_amount: Decimal,
    ):
        if not self.name:
            self.name = name
        self.current_price = current_price
        self.is_on_special = is_on_special
        self.previous_price = previous_price
        self.savings_amount = savings_amount
        self.updated_at = datetime.now(timezone.utc)
        self.save()
