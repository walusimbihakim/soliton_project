from django import template

import projects.models.workers as workers

register = template.Library()

@register.filter
def get_withdraw_charge_filter(amount):
    charge = get_withdraw_charge(amount)    
    
    return charge

def get_withdraw_charge(amount):
    if amount <= 2500:
        charge=330
    elif amount <= 5000:
        charge=440
    elif amount <= 15000:
        charge=700
    elif amount <= 30000:
        charge=880
    elif amount <= 45000:
        charge=1210
    elif amount <= 60000:
        charge=1500
    elif amount <= 125000:
        charge=1925
    elif amount <= 250000:
        charge=3575
    elif amount <= 500000:
        charge=7000
    else:
        charge=12500
    
    return charge

@register.filter
def wage_total_filter(amount):
    charge = get_withdraw_charge(amount)
    wage_total = charge+amount

    return wage_total

@register.filter
def get_worker(worker_id, option):
    worker = workers.Worker.objects.get(pk=worker_id)

    if option==1:
        return worker.name
    elif option==2:
        return worker.mobile_money_number
