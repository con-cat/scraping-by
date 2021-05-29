from decimal import Decimal

from django.db import models


class Product(models.Model):
    # The supermarket's product ID
    ww_id = models.PositiveIntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=128, blank=True, default="")
    # InstorePrice from the API
    current_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    # InstoreIsOnSpecial
    is_on_special = models.BooleanField(default=False)
    # InstoreWasPrice and InstoreSavingsAmount
    previous_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    savings_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        if self.name:
            return f"{self.ww_id}: {self.name}"
        return str(self.ww_id)

    @property
    def discount(self) -> Decimal:
        return self.previous_price / self.savings_amount
