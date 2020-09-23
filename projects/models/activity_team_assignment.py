from django.db import models
from projects.models import Team, Activity, Project


class ActivityTeamAssignment(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    Finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()

    def __str__(self):
        return "{} Activity".format(self.team)