from django.db import models

from projects.models import Worker
from projects.models.field_managers import FieldManager


class Team(models.Model):
    name = models.CharField(max_length=20)
    field_manager = models.ForeignKey(FieldManager, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WorkerTeam(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)






