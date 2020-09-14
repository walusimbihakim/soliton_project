from django.db import models

from clients.selectors import get_activity_client_rate
from projects.models import Activity
from projects.models.materials import Material
from projects.models.survey import Survey



class BOQ(models.Model):
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE)
    description = models.TextField(blank=True)


class MaterialBOQItem(models.Model):
    boq = models.ForeignKey(BOQ, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def cost(self):
        unit_cost = self.material.unit_cost
        cost = unit_cost * self.quantity
        return cost


class ServiceBOQItem(models.Model):
    boq = models.ForeignKey(BOQ, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    description = models.TextField()
    quantity = models.IntegerField()

    @property
    def cost(self):
        unit_cost = get_activity_client_rate(self.activity)
        cost = unit_cost * self.quantity
        return cost
