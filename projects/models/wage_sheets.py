from django.db import models

from projects.models import Worker, FieldManager, Activity
from projects.models.segments import Segment

class WageSheet(models.Model):
    field_manager = models.ForeignKey(FieldManager, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Worker, on_delete=models.CASCADE)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, default=1)
    date = models.DateField()
    description = models.TextField()
    is_submitted = models.BooleanField()
    manager_status = models.BooleanField()
    manager_comment = models.TextField(default="-")
    project_manager_status = models.BooleanField()
    project_manager_comment = models.TextField(default="-")
    gm_status = models.BooleanField()
    gm_comment = models.TextField(default="-")

    class Meta:
        unique_together = ('supervisor', 'field_manager', 'date')

    def __str__(self):
        return f"{self.team} Wage Sheet {self.id}"


class Wage(models.Model):
    wage_sheet = models.ForeignKey(WageSheet, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    payment = models.IntegerField()

    class Meta:
        unique_together = ('worker', 'activity')

    def __str__(self):
        return f"{self.worker} - Wage ID {self.id}"
