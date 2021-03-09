from django import template
import projects.models.workers as workers
from projects.selectors.wage_bill_selectors import get_airtel_money_withdraw_charge

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
def get_worker(worker_id, option):
    worker = workers.Worker.objects.get(pk=worker_id)

    if option == 1:
        return worker.name
    elif option == 2:
        return worker.mobile_money_number
