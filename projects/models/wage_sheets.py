from django.db import models

from projects.models import Team, Project, Worker, PIP


class WageSheet(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date = models.DateField()
    segment = models.CharField(max_length=40)
    description = models.TextField()

    class Meta:
        unique_together = ('team', 'date')

    def __str__(self):
        return f"{self.team} Wage Sheet {self.id}"


class Wage(models.Model):
    wage_sheet = models.ForeignKey(WageSheet, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    pip_activity = models.ForeignKey(PIP, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    payment = models.IntegerField()

    class Meta:
        unique_together = ('worker', 'pip_activity')

    def __str__(self):
        return f"{self.worker} - Wage ID {self.id}"
