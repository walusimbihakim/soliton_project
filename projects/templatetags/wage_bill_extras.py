from django import template

from projects.selectors.wage_bill_selectors import get_airtel_money_withdraw_charge, get_current_wage_bill
from projects.selectors.workers import get_worker
from projects.selectors.complaints import get_worker_complaints

register = template.Library()


@register.filter
def get_withdraw_charge_filter(amount):
    charge = get_airtel_money_withdraw_charge(amount)

    return charge


@register.filter
def wage_total_filter(amount):
    charge = get_airtel_money_withdraw_charge(amount)
    wage_total = charge + amount
    return wage_total


@register.filter
def get_worker_info(worker_id, option):
    worker = get_worker(worker_id)

    if option == 1:
        return worker.name
    elif option == 2:
        return worker.mobile_money_number

@register.filter
def total_payment(worker_id, payment):
    worker = get_worker(worker_id)

    wage_bill = get_current_wage_bill()

    complaint = get_worker_complaints(worker,wage_bill)

    
    return (payment+complaint["payment"])    

