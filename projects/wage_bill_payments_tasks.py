from celery.app import shared_task

from projects.classes.simple_wage_bill_payment import SimpleWageBillPayment
from projects.selectors import wage_bill_selectors
from projects.selectors.workers import get_all_workers
from projects.services.wage_bill_services import create_consolidated_wage_bill


@shared_task
def generate_wage_bill_task_process(wage_bill_id):
    workers = get_all_workers()
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id)
    for worker in workers:
        simple_wage_bill_payment = SimpleWageBillPayment(wage_bill, worker)
        if simple_wage_bill_payment.has_amount_payable:
            create_consolidated_wage_bill(simple_wage_bill_payment)
