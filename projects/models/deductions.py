from django.db import models

from projects.models import Worker, Activity, FieldManager, WageSheet


class Deduction(models.Model):
    CAUSE_CHOICES = [
        ('Fine', 'Fine'),
        ('Damage', 'Damage'),
        ('Overpayment', 'Overpayment'),
    ]
    wage_sheet = models.ForeignKey(WageSheet, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    cause = models.CharField(max_length=12, choices=CAUSE_CHOICES)
    payment = models.IntegerField()
    description = models.TextField(default="")
    is_manager_approved = models.BooleanField(default=True)
    is_pm_approved = models.BooleanField(null=True)
    is_gm_approved = models.BooleanField(null=True)
    is_payed = models.BooleanField(null=True)

    class Meta:
        unique_together = ('worker', 'wage_sheet')

    def __str__(self):
        return f"{self.worker} - Deduction ID {self.id}"
