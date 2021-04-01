import datetime

from projects.selectors import wage_bill_selectors


def set_current_wage_bill_status_to_done() -> bool:
    current_wage_bill = wage_bill_selectors.get_current_wage_bill()

    if current_wage_bill:
        current_wage_bill.status = "Done"
        current_wage_bill.save()
        return True
    else:
        return False


def create_wage_bill_service() -> bool:
    # current_date = date.today()
    # end_date = current_date + datetime.timedelta(days=6)
    # WageBill.objects.create(start_date=current_date, end_date=end_date)
    # return True
    pass
