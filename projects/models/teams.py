from django.db import models

from projects.models import Worker, PIP
from projects.models.field_managers import FieldManager


class Team(models.Model):
    name = models.CharField(max_length=20)
    field_manager = models.ForeignKey(FieldManager, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Worker, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'field_manager', 'supervisor')

    def __str__(self):
        return self.name


class PIPTeam(models.Model):
    pip_activity = models.ForeignKey(PIP, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_work_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("pip_activity", "team")

    def __str__(self):
        return f"{self.pip_activity} - {self.team} Assignment"
