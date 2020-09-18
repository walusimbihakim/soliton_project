from django.db import models
from model_utils.models import TimeStampedModel
from clients.models import Client
from .projects import Project
from .projects.models import activity_list

class PIP(TimeStampedModel):
    scope = models.ForeignKey(Scope, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=50)

class predecessor(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    predecessor = models.ForeignKey(Activity, on_delete=models.CASCADE)
    