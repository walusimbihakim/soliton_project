from projects.models.wage_bills import ConsolidatedWageBill
from projects.selectors import wage_bill_selectors
from projects.selectors.user_selectors import get_users
from projects.tasks import send_wage_created_email_task


def set_current_wage_bill_status_to_done() -> bool:
    current_wage_bill = wage_bill_selectors.get_current_wage_bill()
    if current_wage_bill:
        current_wage_bill.status = "Done"
        current_wage_bill.save()
        return True
    else:
        return False


def send_wage_created_email_service():
    receivers = []
    users = get_users()
    for user in users:
        receivers.append(user.email)
    send_wage_created_email_task.delay(receivers=receivers)


def create_consolidated_wage_bill(simple_wage_bill_payment):
    consolidated_wage_bill = ConsolidatedWageBill.objects.create(
        wage_bill=simple_wage_bill_payment.wage_bill,
        worker_id=simple_wage_bill_payment.worker.id,
        worker_name=simple_wage_bill_payment.worker.name,
        worker_mobile_money_number=simple_wage_bill_payment.worker.mobile_money_number,
        worker_mobile_money_name=simple_wage_bill_payment.worker.name,
        supervisor=simple_wage_bill_payment.worker.registered_by_user.name,
        supervisor_number=simple_wage_bill_payment.worker.registered_by_user.phone_number,
        total_wages=simple_wage_bill_payment.total_wages,
        total_complaints=simple_wage_bill_payment.total_complaints,
        total_deductions=simple_wage_bill_payment.total_deductions
    )
    return consolidated_wage_bill
