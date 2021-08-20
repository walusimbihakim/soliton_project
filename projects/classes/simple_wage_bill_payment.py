from datetime import timedelta

from projects.models import WageBill, Worker
from projects.procedures import calculate_total_wages
from projects.selectors.complaints import get_worker_complaints_payment
from projects.selectors.field_managers import get_field_manager_from_worker, get_the_latest_wage_field_manager
from projects.selectors.wage_bill_selectors import \
    get_wage_bill_worker_wages, \
    get_wage_bill_worker_deductions
from projects.selectors.wage_sheets import get_worker_payment_per_day


class SimpleWageBillPayment:
    #
    def __init__(self, wage_bill: WageBill, worker: Worker):
        self.wage_bill = wage_bill
        self.worker_name = worker.name
        self.supervisor_name = worker.assigned_to.name
        self.worker_mobile_money_number = worker.mobile_money_number
        self.supervisor_mobile_number = worker.assigned_to.phone_number
        self.worker = worker
        self.field_manager = get_the_latest_wage_field_manager(worker)

    @property
    def field_manager_phone_number(self):
        print("The field manager is", self.field_manager)
        if self.field_manager:
            return self.field_manager.phone_number
        return "N/A"

    @property
    def total_wages(self) -> int:
        wages = get_wage_bill_worker_wages(self.wage_bill, self.worker)
        return calculate_total_wages(wages)

    @property
    def total_complaints(self) -> int:
        complaints = get_worker_complaints_payment(self.worker, self.wage_bill)
        return complaints

    @property
    def total_deductions(self) -> int:
        deductions = get_wage_bill_worker_deductions(self.wage_bill, self.worker)
        return calculate_total_wages(deductions)

    @property
    def has_amount_payable(self) -> bool:
        return bool(self.total_wages) or bool(self.total_deductions) or \
               bool(self.total_complaints)

    @property
    def wednesday_total_amount(self) -> int:
        date = self.wage_bill.start_date
        return get_worker_payment_per_day(self.wage_bill, self.worker, date)

    @property
    def thursday_total_amount(self) -> int:
        date = self.wage_bill.start_date + timedelta(days=1)
        return get_worker_payment_per_day(self.wage_bill, self.worker, date)

    @property
    def friday_total_amount(self) -> int:
        date = self.wage_bill.start_date + timedelta(days=2)
        return get_worker_payment_per_day(self.wage_bill, self.worker, date)

    @property
    def saturday_total_amount(self) -> int:
        date = self.wage_bill.start_date + timedelta(days=3)
        return get_worker_payment_per_day(self.wage_bill, self.worker, date)

    @property
    def sunday_total_amount(self) -> int:
        date = self.wage_bill.start_date + timedelta(days=4)
        return get_worker_payment_per_day(self.wage_bill, self.worker, date)

    @property
    def monday_total_amount(self) -> int:
        date = self.wage_bill.start_date + timedelta(days=5)
        return get_worker_payment_per_day(self.wage_bill, self.worker, date)

    @property
    def tuesday_total_amount(self) -> int:
        date = self.wage_bill.end_date
        return get_worker_payment_per_day(self.wage_bill, self.worker, date)
