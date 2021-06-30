import datetime
from datetime import date
from celery import shared_task
from django.db import IntegrityError
from project_manager.celery import app
from projects.classes.mails import WageBillCreatedMail
from projects.models import WageBill
from projects.selectors import wage_bill_selectors
from projects.selectors.user_selectors import get_users
from projects.selectors.wage_bill_selectors import get_current_wage_bill


@app.task
def create_wage_bill():
    current_wage_bill = wage_bill_selectors.get_current_wage_bill()
    if current_wage_bill:
        current_wage_bill.status = "Done"
        current_wage_bill.save()
    current_date = date.today()
    end_date = current_date + datetime.timedelta(days=6)
    try:
        WageBill.objects.create(start_date=current_date, end_date=end_date)
    except IntegrityError as e:
        return "Wage Bill already Created"
    return "Wage Bill Created"


@shared_task
def send_wage_created_email_task():
    wage_bill = get_current_wage_bill()
    users = get_users()
    receiver_emails = []
    for user in users:
        receiver_emails.append(user.email)

    mail = WageBillCreatedMail(wage_bill=wage_bill, receivers=receiver_emails)
    mail.send_email()
