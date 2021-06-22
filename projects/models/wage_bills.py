from django.db import models
from django.urls import reverse

from projects.procedures import calculate_airtel_charge


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

    @property
    def is_payment_generated(self):
        return bool(self.consolidatedwagebill_set.all())

    @property
    def is_wage_bill_week_done(self):
        return self.status == "Done"

    @property
    def total_consolidated_payments(self):
        consolidated_payments = self.consolidatedwagebill_set.all()


class ConsolidatedWageBillPayment(models.Model):
    wage_bill = models.ForeignKey(WageBill, on_delete=models.CASCADE)
    worker_id = models.IntegerField()
    worker_name = models.CharField(max_length=50)
    worker_mobile_money_number = models.CharField(max_length=10, blank=True)
    worker_mobile_money_name = models.CharField(max_length=50, blank=True, null=True)
    supervisor_id = models.IntegerField(null=True, blank=True)
    supervisor = models.CharField(max_length=50, blank=True, null=True)
    supervisor_number = models.CharField(max_length=50, blank=True, null=True)
    total_wages = models.IntegerField(default=0)
    total_complaints = models.IntegerField(default=0)
    total_deductions = models.IntegerField(default=0)
    # Days
    wednesday_total_amount = models.IntegerField(default=0)
    thursday_total_amount = models.IntegerField(default=0)
    friday_total_amount = models.IntegerField(default=0)
    saturday_total_amount = models.IntegerField(default=0)
    sunday_total_amount = models.IntegerField(default=0)
    monday_total_amount = models.IntegerField(default=0)
    tuesday_total_amount = models.IntegerField(default=0)

    class Meta:
        ordering = "supervisor",
        unique_together = ("wage_bill", "worker_id")

    @property
    def total_amount(self):
        return (self.total_wages + self.total_complaints) - self.total_deductions

    @property
    def charge(self):
        return calculate_airtel_charge(self.total_amount)

    @property
    def total_payment(self):
        return self.charge + self.total_amount
