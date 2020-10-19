from django.db import models


class FieldManager(models.Model):
    employee_id = models.CharField(max_length=20)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
