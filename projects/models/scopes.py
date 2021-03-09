from django.db import models

from projects.models import Survey


class ExecutionScope(models.Model):
    quantity = models.IntegerField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return "{} ".format(self.survey)
