from django.db import models
from projects.constants import OFC, ISP, OSP, FINANCIAL, WAREHOUSE, POWER, MAINTENANCE, WORKSHOP, ADMINISTRATOR, \
    SECURITY, MISCELLANEOUS
from projects.models.users import User


class Worker(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    TYPE_CHOICES = [
        (ISP, ISP),
        (OFC, OFC),
        (OSP, OSP),
        (FINANCIAL, FINANCIAL),
        (WAREHOUSE, WAREHOUSE),
        (POWER, POWER),
        (MAINTENANCE, MAINTENANCE),
        (WORKSHOP, WORKSHOP),
        (ADMINISTRATOR, ADMINISTRATOR),
        (SECURITY, SECURITY),
        (MISCELLANEOUS, MISCELLANEOUS)
    ]

    BUSINESS_UNIT_CHOICES = [
        ('MS', 'Managed Services'),
        ('CN', 'Connectivity'),
        ('ND', 'Network Deployment'),
        ('QL', 'Quality'),
        ('ET', 'Emerging Technologies'),
        ('SU', 'Support')
    ]
    name = models.CharField(max_length=50)
    national_ID_NIN = models.CharField(max_length=20)
    joining_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    mobile_money_number = models.CharField(max_length=10, unique=True)
    mobile_money_name = models.CharField(max_length=30)
    address = models.CharField(max_length=15)
    next_of_kin = models.CharField(max_length=60, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    business_unit = models.CharField(
        max_length=2, choices=BUSINESS_UNIT_CHOICES)
    national_ID_document = models.FileField(upload_to="documents")
    profile = models.FileField(upload_to="documents")
    registered_by_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Currently Working Under",
        blank=True, null=True,
        related_name="Assignments"
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class WorkerAssignment(models.Model):
    date = models.DateField(auto_now_add=True)
    worker = models.ForeignKey(Worker, on_delete=models.DO_NOTHING)
    from_supervisor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    to_supervisor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                      related_name="to_supervisor")

    class Meta:
        verbose_name = ("WorkerAssignment")
        verbose_name_plural = ("WorkerAssignments")


class GroupWorker(models.Model):
    name = models.CharField(max_length=20, unique=True)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    workers = models.ManyToManyField(Worker)

    def __str__(self):
        return self.name

    @property
    def get_all_workers(self):
        return self.workers.all()
