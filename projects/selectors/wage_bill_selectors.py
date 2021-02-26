from django.db.models import Sum
import projects.models.wage_bills as wage_bills
import projects.models.wage_sheets as wage_sheets


def get_wage_bills():
    return wage_bills.WageBill.objects.all()


def get_wage_bill(wage_bill_id):
    return wage_bills.WageBill.objects.get(pk=wage_bill_id)


def get_current_wage_bill():
    return wage_bills.WageBill.objects.get(status="Current")


def get_wage_bill_sheets(wage_bill):
    return wage_sheets.WageSheet.objects.filter(wage_bill=wage_bill)


def get_wage_bill_wages(wage_bill):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)

    return wage_sheets.Wage.objects.filter(wage_sheet__in=wage_bill_sheets, is_gm_approved=True)


def get_aggregated_wage_bill(wage_bill):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)

    aggregated_wages = wage_sheets.Wage.objects \
        .filter(wage_sheet__in=wage_bill_sheets, is_gm_approved=True) \
        .values("worker").annotate(payment=Sum("payment"))
    return aggregated_wages


def get_airtel_money_withdraw_charge(amount: int) -> int:
    if amount <= 2500:
        charge = 330
    elif amount <= 5000:
        charge = 440
    elif amount <= 15000:
        charge = 700
    elif amount <= 30000:
        charge = 880
    elif amount <= 45000:
        charge = 1210
    elif amount <= 60000:
        charge = 1500
    elif amount <= 125000:
        charge = 1925
    elif amount <= 250000:
        charge = 3575
    elif amount <= 500000:
        charge = 7000
    else:
        charge = 12500

    return charge
