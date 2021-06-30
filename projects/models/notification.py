from django.db import models

from projects.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE),
    title = models.CharField(max_length=40),
    message = models.CharField(max_length=200),
    is_read = models.BooleanField(default=False),
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.title}"
