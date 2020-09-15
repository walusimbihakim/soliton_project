from django.db import models


class Material(models.Model):
    CURRENCY_CHOICES = [
        ("USD", "USD"),
        ("UGX", "UGX")
    ]
    name = models.CharField(max_length=20)
    uom = models.CharField(max_length=20)
    unit_cost = models.IntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)

    def __str__(self):
        return self.name
