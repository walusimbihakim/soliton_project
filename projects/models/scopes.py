from django.db import models

from projects.models import Survey


class ExecutionScope(models.Model):
    quantity = models.IntegerField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    description = models.TextField()

    class Meta:
        unique_together = ("quantity", "survey")

    def __str__(self):
        return "{} Execution Scope".format(self.survey)
