from django.db import models

from projects.models import Worker, Activity,  WageSheet


class Complaint(models.Model):
    wage_sheet = models.ForeignKey(WageSheet, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    payment = models.IntegerField()
    description = models.TextField(default="")
    is_manager_approved = models.BooleanField(default=True)
    is_pm_approved = models.BooleanField(null=True)
    is_gm_approved = models.BooleanField(null=True)
    is_payed = models.BooleanField(null=True)
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('worker', 'wage_sheet', 'activity')

    def __str__(self):
        return f"{self.worker} - Complaint ID {self.id}"
