from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel
from projects.models.project_settings import UnitOfMeasure


class Activity(TimeStampedModel):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=150)
    unit_cost = models.IntegerField(default=0)
    unit_of_measure = models.ForeignKey(UnitOfMeasure, on_delete=models.CASCADE, blank=True, null=True)
    is_fd_underground = models.BooleanField(default=False, blank=True, null=True)
    is_fd_arial = models.BooleanField(default=False, blank=True, null=True)
    is_site_connection = models.BooleanField(default=False, blank=True, null=True)
    is_tower_construction = models.BooleanField(default=False, blank=True, null=True)
    is_lan_installation = models.BooleanField(default=False, blank=True, null=True)
    is_equipment_installation = models.BooleanField(default=False, blank=True, null=True)
    is_manhole_installation = models.BooleanField(default=False, blank=True, null=True)


    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Activity_detail", kwargs={"pk": self.pk})



