from django.db import models


# Create your models here.


class Client(models.Model):
    company_name = models.CharField(max_length=30)
    address = models.CharField(max_length=50,blank=True)
    email = models.EmailField(max_length=254, blank=True)
    contact = models.CharField(max_length=15, blank=True)
    website = models.URLField(max_length=45, blank=True)
    contact_person = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.company_name


class ClientContacts(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=10)
    contact = models.CharField(max_length=50)
