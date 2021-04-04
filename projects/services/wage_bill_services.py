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
    send_wage_created_email_task(receivers=receivers)
