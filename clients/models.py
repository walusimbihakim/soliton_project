from django.db import models


# Create your models here.
class Client(models.Model):
    company_name = models.CharField(max_length=30)
    address = models.TextField()
    email = models.EmailField(max_length=254, default="null")
    contact = models.CharField(max_length=15, default="null")
    website = models.CharField(max_length=45)
    contact_person = models.CharField(max_length=45)
    profile_pic = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.company_name


class ClientContacts(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=10)
    contact = models.CharField(max_length=50)
