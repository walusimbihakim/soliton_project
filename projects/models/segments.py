from django.db import models
from projects.models.scopes import ExecutionScope

class Segment(models.Model):
    name = models.CharField(max_length=50)
    execution_scope = models.ForeignKey(ExecutionScope, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name
