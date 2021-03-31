import datetime
from datetime import date
from django.db import IntegrityError
from project_manager.celery import app
from projects.models import WageBill
from projects.services.wage_bill_services import set_current_wage_bill_status_to_done


@app.task
def create_wage_bill():
    set_current_wage_bill_status_to_done()
    current_date = date.today()
    end_date = current_date + datetime.timedelta(days=6)
    try:
        WageBill.objects.create(start_date=current_date, end_date=end_date)
    except IntegrityError as e:
        return "Wage Bill already Created"

    return "Wage Bill Created"
