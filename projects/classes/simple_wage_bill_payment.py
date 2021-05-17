from projects.models import WageBill, Worker
from projects.procedures import calculate_total_wages
from projects.selectors.wage_bill_selectors import get_wage_bill_worker_wages, \
    get_wage_bill_worker_complaints, get_wage_bill_worker_deductions


class SimpleWageBillPayment:

    def __init__(self, wage_bill: WageBill, worker: Worker):
        self.wage_bill = wage_bill
        self.worker_name = worker.name
        self.supervisor_name = worker.registered_by_user
        self.worker_mobile_money_number = worker.mobile_money_number
        self.supervisor_mobile_number = worker.registered_by_user.phone_number
        self.worker = worker

    @property
    def total_wages(self) -> int:
        wages = get_wage_bill_worker_wages(self.wage_bill, self.worker)
        return calculate_total_wages(wages)

    @property
    def total_complaints(self) -> int:
        complaints = get_wage_bill_worker_complaints(self.wage_bill, self.worker)
        return calculate_total_wages(complaints)

    @property
    def total_deductions(self) -> int:
        deductions = get_wage_bill_worker_deductions(self.wage_bill, self.worker)
        return calculate_total_wages(deductions)

    @property
    def has_amount_payable(self) -> bool:
        return bool(self.total_wages) or bool(self.total_deductions) or \
               bool(self.total_complaints)
