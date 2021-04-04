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
        wage_bill = WageBill.objects.create(start_date=current_date, end_date=end_date)
        receivers = get_users()
        send_wage_created_email_task.delay(wage_bill=wage_bill, receivers=receivers)
    except IntegrityError as e:
        return "Wage Bill already Created"
    return "Wage Bill Created"


@shared_task
def send_wage_created_email_task(receivers: list):
    wage_bill = get_current_wage_bill()
    mail = WageBillCreatedMail(wage_bill=wage_bill, receivers=receivers)
    mail.create_mail()
    mail.send_email()
    print("receivers", mail.get_receivers())
    print("context", mail.context)
    print("template_uri", mail.get_template_uri())
