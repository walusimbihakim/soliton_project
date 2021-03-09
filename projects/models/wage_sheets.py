from django.db import models

from projects.models import Worker, FieldManager, Activity
from projects.models.segments import Segment
from projects.models.wage_bills import WageBill


class WageSheet(models.Model):
    wage_bill = models.ForeignKey(WageBill, on_delete=models.CASCADE, default=None, null=True)
    field_manager = models.ForeignKey(FieldManager, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Worker, on_delete=models.CASCADE)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    description = models.TextField()
    is_submitted = models.BooleanField(default=False)
    manager_status = models.BooleanField(null=True)
    manager_comment = models.TextField(default="-")
    project_manager_status = models.BooleanField(null=True)
    project_manager_comment = models.TextField(default="-")
    gm_status = models.BooleanField(null=True)
    gm_comment = models.TextField(default="-")

    class Meta:
        unique_together = ('supervisor', 'field_manager', 'date')

    def __str__(self):
        return f"{self.supervisor} Wage Sheet {self.id}"


class Wage(models.Model):
    wage_sheet = models.ForeignKey(WageSheet, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    payment = models.IntegerField()
    is_manager_approved = models.BooleanField(default=True)
    is_pm_approved = models.BooleanField(null=True)
    is_gm_approved = models.BooleanField(null=True)
    is_payed = models.BooleanField(null=True)

    class Meta:
        unique_together = ('worker', 'activity')

    def __str__(self):
        return f"{self.worker} - Wage ID {self.id}"
