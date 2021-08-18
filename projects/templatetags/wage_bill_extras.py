from django.db.models.aggregates import Count
from django import template
from django.db.models import Sum, manager

from projects.selectors.wage_bill_selectors import (
    get_airtel_money_withdraw_charge, 
    get_current_wage_bill,
    get_wage_bill_sheets,
    get_wage_bill
)
from projects.selectors.workers import get_worker
from projects.selectors.complaints import get_worker_complaints_payment
from projects.models.wage_sheets import Wage
from projects.selectors.user_selectors import get_user_by_id

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
    complaints_payment = get_worker_complaints_payment(worker, wage_bill)
    return payment + complaints_payment

@register.filter
def get_manager_name(manager_id):
    manager = get_user_by_id(manager_id)

    return manager.name

@register.filter
def get_wage_bill_total(wage_bill):
    
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)
    
    sheet_total = Wage.objects.filter(
        wage_sheet__in=wage_bill_sheets, is_manager_approved=True
        ).aggregate(total = Sum('payment'))
    return sheet_total['total']

@register.filter
def get_wage_bill_casuals(wage_bill_id):
    wage_bill = get_wage_bill(wage_bill_id)

    casuals = wage_bill.consolidatedwagebillpayment_set.all().aggregate(total = Count("worker_id"))

    return casuals['total']
