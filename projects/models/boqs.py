from django.db import models

from projects.models import Activity
from projects.models.materials import Material


class BOQ(models.Model):
    description = models.TextField()


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
    Description = models.TextField()
    quantity = models.IntegerField()

    @property
    def cost(self):
        unit_cost = self.material.unit_cost
        cost = unit_cost * self.quantity
        return cost
