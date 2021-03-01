from django.db import models
from django.shortcuts import reverse


class User(models.Model):

    role_options = [
        ("Supervisor", "Supervisor"),
        ("Manager", "Manager"),
        ("PM", "Project Manager"),
        ("GM", "General Manager")
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    username = models.CharField(unique=True, max_length=50)
    user_role = models.CharField(max_length=50, choices=role_options)
    password = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})


class LoginLog(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateField(auto_now_add=True)
    login_time = models.TimeField(auto_now_add=True)
    logout_date = models.DateField(auto_now_add=True)
    logout_time = models.TimeField(auto_now_add=True)
    is_success = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("LoginLog")
        verbose_name_plural = ("LoginLogs")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("LoginLog_detail", kwargs={"pk": self.pk})
