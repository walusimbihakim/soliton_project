from django.db import models
from django.urls import reverse
from projects.models.workers import Worker


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
        start_date_str = self.start_date.strftime("%d %b %Y")
        end_date_str = self.end_date.strftime("%d %b %Y")
        return f"{start_date_str} - {end_date_str}"

    def get_absolute_url(self):
        return reverse("WageBill_detail", kwargs={"pk": self.pk})

class ConsolidatedWageBill(models.Model):

    wage_bill = models.ForeignKey(WageBill, on_delete=models.DO_NOTHING)
    worker = models.ForeignKey(Worker, on_delete=models.DO_NOTHING)
    mobile_money_number = models.IntegerField()
    amount = models.IntegerField()
    charge = models.IntegerField()
    
    @property
    def total(self):
        total = self.amount + self.charge

        return total


    class Meta:
        verbose_name = ("ConsolidatedWageBill")
        verbose_name_plural = ("ConsolidatedWageBills")

    def __str__(self):
        return self.wage_bill

    def get_absolute_url(self):
        return reverse("ConsolidatedWageBill_detail", kwargs={"pk": self.pk})

