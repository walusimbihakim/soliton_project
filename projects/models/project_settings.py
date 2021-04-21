from django.db import models

class UnitOfMeasure(models.Model):
    unit_of_measure = models.CharField(max_length=50, default="Meter")
    description = models.TextField(null=True)

    def __str__(self):
        return self.unit_of_measure
        
    