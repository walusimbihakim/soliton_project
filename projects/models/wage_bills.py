from django.db import models
from django.urls import reverse
import calendar


class WageBill(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, default="Current")

    class Meta:
        verbose_name = ("WageBill")
        verbose_name_plural = ("WageBills")

        unique_together = ('start_date', 'end_date')
        ordering = ["status"]

    def __str__(self):
        start_month = calendar.month_abbr[self.start_date.month]
        end_month = calendar.month_abbr[self.end_date.month]

        if start_month == end_month:
            return f"{self.start_date.day}th - {self.end_date.day}th {end_month} - {self.end_date.year}"
        else:
            return f"{self.start_date.day}th {start_month} - {self.end_date.day}th {end_month} - {self.end_date.year}"

    def get_absolute_url(self):
        return reverse("WageBill_detail", kwargs={"pk": self.pk})
