from django.db import models
from model_utils.models import TimeStampedModel
from projects.models.activity_list import Activity
from projects.models.scopes import ExecutionScope


class PIP(TimeStampedModel):
    scope = models.ForeignKey(ExecutionScope, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.activity} Activity - {self.scope} Scope - {self.scope.survey} Survey -" \
               f"{self.scope.survey.project} Project"


class Predecessor(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    predecessor = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="activty_dependecies")
