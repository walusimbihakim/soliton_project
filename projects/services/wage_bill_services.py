from projects.models.wage_bills import ConsolidatedWageBillPayment
from projects.selectors import wage_bill_selectors
from projects.selectors.user_selectors import get_users
from projects.selectors.wage_bill_selectors import get_wage_bill
from projects.tasks.random import send_wage_created_email_task


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
    consolidated_wage_bill = ConsolidatedWageBillPayment.objects.create(
        wage_bill=simple_wage_bill_payment.wage_bill,
        worker_id=simple_wage_bill_payment.worker.id,
        worker_name=simple_wage_bill_payment.worker.name,
        worker_mobile_money_number=simple_wage_bill_payment.worker.mobile_money_number,
        wednesday_total_amount=simple_wage_bill_payment.wednesday_total_amount,
        thursday_total_amount=simple_wage_bill_payment.thursday_total_amount,
        friday_total_amount=simple_wage_bill_payment.friday_total_amount,
        saturday_total_amount=simple_wage_bill_payment.saturday_total_amount,
        sunday_total_amount=simple_wage_bill_payment.sunday_total_amount,
        monday_total_amount=simple_wage_bill_payment.monday_total_amount,
        tuesday_total_amount=simple_wage_bill_payment.tuesday_total_amount,
        worker_mobile_money_name=simple_wage_bill_payment.worker.mobile_money_name,
        supervisor=simple_wage_bill_payment.worker.assigned_to.name,
        supervisor_number=simple_wage_bill_payment.worker.assigned_to.phone_number,
        field_manager=simple_wage_bill_payment.field_manager,
        field_manager_number=simple_wage_bill_payment.field_manager_phone_number,
        total_wages=simple_wage_bill_payment.total_wages,
        total_complaints=simple_wage_bill_payment.total_complaints,
        total_deductions=simple_wage_bill_payment.total_deductions
    )
    return consolidated_wage_bill


def remove_all_wage_bill_payments(wage_bill_id):
    wage_bill = get_wage_bill(wage_bill_id)
    ConsolidatedWageBillPayment.objects.filter(wage_bill=wage_bill).delete()
