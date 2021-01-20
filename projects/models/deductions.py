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
    amount = models.IntegerField()
    description = models.TextField(default="")

    class Meta:
        unique_together = ('worker', 'wage_sheet')

    def __str__(self):
        return f"{self.worker} - Deduction ID {self.id}"
