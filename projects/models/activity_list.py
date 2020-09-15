from django.db import models
from model_utils.models import TimeStampedModel
from clients.models import Client
from .projects import Project


class Activity(TimeStampedModel):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=150)
    unit_measure = models.CharField(max_length=10, blank=True, null=True)
    is_fd_underground = models.BooleanField(default=False, blank=True, null=True)
    is_fd_arial = models.BooleanField(default=False, blank=True, null=True)
    is_site_connection = models.BooleanField(default=False, blank=True, null=True)
    is_tower_construction = models.BooleanField(default=False, blank=True, null=True)
    is_lan_installation = models.BooleanField(default=False, blank=True, null=True)
    is_equipment_installation = models.BooleanField(default=False, blank=True, null=True)
    is_manhole_installation = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name = ("Activity")
        verbose_name_plural = ("Activitys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Activity_detail", kwargs={"pk": self.pk})



