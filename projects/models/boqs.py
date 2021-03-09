from django.db import models

from projects.models import Activity
from projects.models.materials import Material
from projects.models.survey import Survey
from projects.selectors.client_activity_rate import get_client_activity_rate, get_client_activity_currency


class BOQ(models.Model):
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE)
    description = models.TextField(blank=True)


class MaterialBOQItem(models.Model):
    boq = models.ForeignKey(BOQ, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('boq', 'material',)

    def __str__(self):
        return f"{self.material}"


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

    class Meta:
        unique_together = ('boq', 'activity',)

    def __str__(self):
        return self.activity.name

    @property
    def unit_cost(self):
        client = self.boq.survey.project.client
        unit_cost = get_client_activity_rate(client, self.activity)
        return unit_cost

    @property
    def cost(self):
        cost = self.unit_cost * self.quantity
        return cost

    @property
    def currency(self):
        client = self.boq.survey.project.client
        currency = get_client_activity_currency(client, self.activity)
        return currency
