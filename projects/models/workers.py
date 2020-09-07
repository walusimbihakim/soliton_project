from django.db import models


class Worker(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    ROLE_CHOICES = [
        ('Supervisor', 'Supervisor'),
        ('Operator', 'Operator'),
        ('ISP', 'ISP'),
        ('OFC', 'OFC'),
        ('Financial', 'Financial'),
    ]
    BUSINESS_UNIT_CHOICES = [
        ('MS', 'Managed Services'),
        ('CN', 'Connectivity'),
        ('ND', 'Network Deployment'),
        ('QL', 'Quality'),
        ('ET', 'Emerging Technologies'),
    ]

    name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=20, unique=True)
    joining_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact = models.CharField(max_length=10)
    address = models.CharField(max_length=15)
    next_of_kin = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    business_unit = models.CharField(max_length=2, choices=BUSINESS_UNIT_CHOICES)
    national_id_document = models.FileField(upload_to="documents")

    def __str__(self):
        return self.name




