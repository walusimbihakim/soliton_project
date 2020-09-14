from django.db import models
from clients.models import Client
from projects.models import Activity


class ClientActivityPrice(models.Model):
    CURRENCY_CHOICES = [
        ("USD", "USD"),
        ("UGX", "UGX")
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    cost = models.IntegerField(default=0)
    currency = models.CharField(max_length=3, default="UGX", choices=CURRENCY_CHOICES)
