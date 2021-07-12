from django.db import models, IntegrityError

from projects.models import Worker, Activity, GroupWorker
from projects.models.segments import Segment
from projects.models.wage_bills import WageBill
from projects.models.users import User
from projects.procedures import calculate_total_wages


class WageSheet(models.Model):
    wage_bill = models.ForeignKey(WageBill, on_delete=models.CASCADE, default=None, null=True)
    field_manager_user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_manager_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                             related_name="wage_sheet_project_manager")
    supervisor_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wage_sheet_supervisor")
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    description = models.TextField()
    is_submitted = models.BooleanField(default=False)
    manager_status = models.BooleanField(null=True)
    manager_comment = models.TextField(default="-", null=True, blank=True)
    project_manager_status = models.BooleanField(null=True)
    project_manager_comment = models.TextField(default="-", null=True, blank=True)
    gm_status = models.BooleanField(null=True)
    gm_comment = models.TextField(default="-", null=True, blank=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    supervisor_submission_time = models.DateTimeField(null=True, blank=True)
    field_manager_approval_time = models.DateTimeField(null=True, blank=True)
    project_manager_approval_time = models.DateTimeField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)

    @property
    def total_wages(self) -> int:
        wage_queryset = self.wage_set.all()
        wages = calculate_total_wages(wage_queryset)
        return wages

    @property
    def total_complaints(self) -> int:
        complaint_queryset = self.complaint_set.all()
        complaints = calculate_total_wages(complaint_queryset)
        return complaints
 
    @property
    def total_deductions(self) -> int:
        deduction_queryset = self.deduction_set.all()
        deductions = calculate_total_wages(deduction_queryset)
        return deductions

    @property
    def total_amount(self) -> int:
        return (self.total_wages + self.total_complaints) - self.total_deductions

    class Meta:
        ordering = ("supervisor_user__first_name",)
        unique_together = ('supervisor_user', 'field_manager_user', 'date', 'wage_bill')

    def __str__(self):
        return f"{self.supervisor_user} Wage Sheet {self.id}"

    @property
    def is_field_manager_pending(self):
        return self.manager_status is None

    @property
    def is_project_manager_pending(self):
        return self.project_manager_status is None

    @property
    def is_general_manager_pending(self):
        return self.gm_status is None


class GroupWage(models.Model):
    wage_sheet = models.ForeignKey(WageSheet, on_delete=models.CASCADE)
    group_worker = models.ForeignKey(GroupWorker, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    payment = models.IntegerField()

    class Meta:
        unique_together = ("wage_sheet", "group_worker", "activity",)

    def __str__(self):
        return f"{self.group_worker} - Group Wage ID {self.id}"

    def save(self, *args, **kwargs):
        workers = self.group_worker.workers.all()
        number_of_workers = workers.count()
        for worker in workers:
            worker_payment = int(self.payment) / int(number_of_workers)
            try:
                Wage.objects.create(
                    wage_sheet=self.wage_sheet,
                    worker=worker,
                    activity=self.activity,
                    quantity=self.quantity,
                    payment=worker_payment,
                )
            except IntegrityError:
                Wage.objects.filter(
                    wage_sheet=self.wage_sheet,
                    activity=self.activity, ).update(
                    quantity=self.quantity,
                    payment=worker_payment,
                )
        super(GroupWage, self).save(*args, **kwargs)


class Wage(models.Model):
    wage_sheet = models.ForeignKey(WageSheet, on_delete=models.CASCADE)
    group_wage = models.ForeignKey(GroupWage, on_delete=models.CASCADE, null=True, blank=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    payment = models.IntegerField()
    is_manager_approved = models.BooleanField(default=True)
    is_pm_approved = models.BooleanField(null=True)
    is_gm_approved = models.BooleanField(null=True)
    is_payed = models.BooleanField(null=True)
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("worker__name",)
        unique_together = ('worker', 'activity', 'wage_sheet')

    def __str__(self):
        return f"{self.worker} - Wage ID {self.id}"
