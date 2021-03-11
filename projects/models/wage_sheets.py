from django.db import models

from projects.models import Worker, Activity
from projects.models.segments import Segment
from projects.models.wage_bills import WageBill
from projects.models.users import User


class WageSheet(models.Model):
    wage_bill = models.ForeignKey(WageBill, on_delete=models.CASCADE, default=None, null=True)
    field_manager_user = models.ForeignKey(User, on_delete=models.CASCADE)
    supervisor_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wage_sheet_supervisor")
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    description = models.TextField()
    is_submitted = models.BooleanField(default=False)
    manager_status = models.BooleanField(null=True)
    manager_comment = models.TextField(default="-", null=True, blank=True)
    project_manager_status = models.BooleanField(null=True)
    project_manager_comment = models.TextField(default="-", null=True, blank=True)
    gm_status = models.BooleanField(null=True)
    gm_comment = models.TextField(default="-", null=True, blank=True)

    class Meta:
        unique_together = ('supervisor_user', 'field_manager_user', 'date')

    def __str__(self):
        return f"{self.supervisor_user} Wage Sheet {self.id}"


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
