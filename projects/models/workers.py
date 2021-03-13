from django.db import models

from projects.models.users import User


class Worker(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    TYPE_CHOICES = [
        ('ISP', 'ISP'),
        ('OFC', 'OFC'),
        ('Financial', 'Financial'),
        ('Warehouse', 'Warehouse'),
        ('Power', 'Power'),
        ('Maintenance', 'Maintenance'),
        ('Workshop', 'Workshop'),
        ('Administrator', 'Administrator'),
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
    national_id = models.CharField(max_length=20, blank=True)
    joining_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    mobile_money_number = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=15)
    next_of_kin = models.CharField(max_length=15, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    business_unit = models.CharField(
        max_length=2, choices=BUSINESS_UNIT_CHOICES)
    national_id_document = models.FileField(upload_to="documents", blank=True)
    profile = models.FileField(upload_to="documents", blank=True)
    mobile_money_name = models.CharField(max_length=50, null=True, blank=True)
    registered_by_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
