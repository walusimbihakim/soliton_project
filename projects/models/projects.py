from django.db import models
from model_utils.models import TimeStampedModel
from clients.models import Client


class Project(TimeStampedModel):
    project_code = models.CharField("Code", max_length=10, unique=True)
    name = models.CharField("Project Name", max_length=50, unique=True)
    client = models.ForeignKey(Client, verbose_name="Client Company", on_delete=models.CASCADE)
    description = models.CharField("Description", max_length=255, null=True, blank=True)
    start_date = models.DateField("Start Date")
    expected_end_date = models.DateField("Expected End Date")
    status_choices = (
        ('started', 'Started'),
        ('on_going', 'On Going'),
        ('on_hold', 'On Hold'),
        ('success', 'Success'),
        ('canceled', 'Canceled'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default="Started", null=True, blank=True)
    progress = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = ("Project")
        verbose_name_plural = ("Projects")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Project_detail", kwargs={"pk": self.pk})

class ProjectType(models.Model):

    code = models.CharField(max_length=5)
    project_type = models.CharField(max_length=50)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = ("ProjectType")
        verbose_name_plural = ("ProjectTypes")

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("ProjectType_detail", kwargs={"pk": self.pk})

class DuctSystem(models.Model):

    duct_code = models.CharField(max_length=15, default="DC")
    duct_type = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = ("DuctSystem")
        verbose_name_plural = ("DuctSystems")

    def __str__(self):
        return self.duct_code

    def get_absolute_url(self):
        return reverse("DuctSystem_detail", kwargs={"pk": self.pk})

class ProjectWorks(models.Model):

    region_choices = (
        ('central', 'Central'),
        ('northern', 'Northern'),
        ('southern', 'Southern'),
        ('western', 'Western'),
        ('eastern', 'Eastern'),
    )
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    region = models.CharField(choices=region_choices, max_length=50)
    location = models.CharField(max_length=200)
    work_type = models.ForeignKey("projects.ProjectType", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_measure = models.CharField(max_length=50)
    client_segmate = models.CharField(max_length=50, null=True, blank=True)


    class Meta:
        verbose_name = ("ProjectWorks")
        verbose_name_plural = ("ProjectWorks")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ProjectWorks_detail", kwargs={"pk": self.pk})

