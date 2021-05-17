from django.db.models import Sum
import projects.models.wage_bills as wage_bills
import projects.models.wage_sheets as wage_sheets
import projects.models.complaints as complaints
import projects.models.deductions as deductions


def get_wage_bills():
    return wage_bills.WageBill.objects.all().order_by('-id')


def get_wage_bill(wage_bill_id):
    return wage_bills.WageBill.objects.get(pk=wage_bill_id)


def get_current_wage_bill():
    try:
        wage_bill = wage_bills.WageBill.objects.get(status="Current")
    except wage_bills.WageBill.DoesNotExist:
        wage_bill = None
    return wage_bill


def get_wage_bill_sheets(wage_bill):
    return wage_sheets.WageSheet.objects.filter(wage_bill=wage_bill)


def get_wage_bill_wages(wage_bill):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)

    return wage_sheets.Wage.objects.filter(wage_sheet__in=wage_bill_sheets, is_gm_approved=True)


def get_wage_bill_worker_wages(wage_bill, worker):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)

    return wage_sheets.Wage.objects.filter(wage_sheet__in=wage_bill_sheets, worker=worker, is_gm_approved=True)


def get_wage_bill_worker_complaints(wage_bill, worker):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)

    return complaints.Complaint.objects.filter(wage_sheet__in=wage_bill_sheets, worker=worker, is_gm_approved=True)


def get_wage_bill_worker_deductions(wage_bill, worker):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)

    return deductions.Deduction.objects.filter(wage_sheet__in=wage_bill_sheets, worker=worker, is_gm_approved=True)


def get_aggregated_wage_bill(wage_bill):
    wage_bill_wages = get_wage_bill_wages(wage_bill)
    aggregated_wages = wage_bill_wages.values("worker").annotate(payment=Sum("payment")).order_by("worker")
    return aggregated_wages


def get_worker_wage_bill_breakdown(wage_bill, worker):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)
    worker_wage_bill_wages = wage_sheets.Wage.objects.filter(wage_sheet__in=wage_bill_sheets, worker=worker)

    return worker_wage_bill_wages


def get_worker_complaint_breakdown(wage_bill, worker):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)
    worker_wage_bill_wages = complaints.Complaint.objects.filter(wage_sheet__in=wage_bill_sheets, worker=worker)

    return worker_wage_bill_wages


def get_worker_deduction_breakdown(wage_bill, worker):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)
    worker_wage_bill_wages = deductions.Deduction.objects.filter(wage_sheet__in=wage_bill_sheets, worker=worker)
    return worker_wage_bill_wages


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


def get_all_consolidated_wage_bill_payments(wage_bill):
    return wage_bills.ConsolidatedWageBill.objects.filter(wage_bill=wage_bill)