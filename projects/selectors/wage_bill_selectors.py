from projects.procedures import calculate_total_wages
from django.db.models import Sum, Count
import projects.models.wage_bills as wage_bills
import projects.models.wage_sheets as wage_sheets
import projects.models.complaints as complaints
import projects.models.deductions as deductions


def get_wage_bills():
    return wage_bills.WageBill.objects.all().order_by('-id')


def get_wage_bill(wage_bill_id):
    return wage_bills.WageBill.objects.get(pk=wage_bill_id)


def get_current_wage_bill() -> wage_bills.WageBill:
    try:
        wage_bill = wage_bills.WageBill.objects.get(status="Current")
    except wage_bills.WageBill.DoesNotExist:
        wage_bill = None
    return wage_bill


def get_wage_bill_sheets(wage_bill):
    return wage_sheets.WageSheet.objects.filter(wage_bill=wage_bill, project_manager_status=True)


def get_wage_bill_sheets_per_day(wage_bill, date):
    return wage_sheets.WageSheet.objects.filter(wage_bill=wage_bill, date=date, project_manager_status=True)


def get_wage_bill_wages(wage_bill):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)

    return wage_sheets.Wage.objects.filter(wage_sheet__in=wage_bill_sheets, is_gm_approved=True)


def get_wage_bill_worker_wages(wage_bill, worker):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)
    return wage_sheets.Wage.objects.filter(
        wage_sheet__in=wage_bill_sheets,
        worker=worker,
        is_gm_approved=True
    )


def get_wage_bill_worker_wages_per_day(wage_bill, worker, date):
    wage_bill_sheets = get_wage_bill_sheets_per_day(wage_bill, date)
    return wage_sheets.Wage.objects.filter(wage_sheet__in=wage_bill_sheets, worker=worker, is_gm_approved=True)


def get_wage_bill_worker_complaints_per_day(wage_bill, worker, date):
    """Get Approved Complaints amount payable to worker per day"""
    wage_bill_sheets = get_wage_bill_sheets_per_day(wage_bill, date)
    return complaints.Complaint.objects.filter(
        wage_sheet__in=wage_bill_sheets,
        worker=worker,
        is_gm_approved=True
    )


def get_wage_bill_worker_deductions(wage_bill, worker):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)
    return deductions.Deduction.objects.filter(
        wage_sheet__in=wage_bill_sheets, worker=worker, is_gm_approved=True)


def get_wage_bill_worker_deductions_per_day(wage_bill, worker, date):
    wage_bill_sheets = get_wage_bill_sheets_per_day(wage_bill, date)
    return deductions.Deduction.objects.filter(wage_sheet__in=wage_bill_sheets, worker=worker, is_gm_approved=True)


def get_aggregated_wage_bill(wage_bill):
    wage_bill_wages = get_wage_bill_wages(wage_bill)
    aggregated_wages = wage_bill_wages.values("worker").annotate(payment=Sum("payment")).order_by("worker")
    return aggregated_wages


def get_worker_wage_bill_breakdown(wage_bill, worker):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)
    worker_wage_bill_wages = wage_sheets.Wage.objects.filter(wage_sheet__in=wage_bill_sheets, worker=worker,
                                                             is_gm_approved=True)

    return worker_wage_bill_wages


def get_wage_bill_payment_breakdown(wage_bill):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)
    wage_bill_wages = wage_sheets.Wage.objects.filter(wage_sheet__in=wage_bill_sheets,
                                                      is_gm_approved=True)

    return wage_bill_wages


def get_worker_complaint_breakdown(wage_bill, worker):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)
    worker_wage_bill_wages = complaints.Complaint.objects.filter(wage_sheet__in=wage_bill_sheets, worker=worker,
                                                                 is_gm_approved=True)

    return worker_wage_bill_wages


def get_complaint_breakdown(wage_bill):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)
    wage_bill_wages = complaints.Complaint.objects.filter(wage_sheet__in=wage_bill_sheets,
                                                          is_gm_approved=True)

    return wage_bill_wages


def get_worker_deduction_breakdown(wage_bill, worker):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)
    worker_wage_bill_wages = deductions.Deduction.objects.filter(wage_sheet__in=wage_bill_sheets, worker=worker,
                                                                 is_gm_approved=True)
    return worker_wage_bill_wages


def get_deduction_breakdown(wage_bill):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)
    worker_wage_bill_wages = deductions.Deduction.objects.filter(wage_sheet__in=wage_bill_sheets, is_gm_approved=True)
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
    return wage_bills.ConsolidatedWageBillPayment.objects.filter(wage_bill=wage_bill)


def get_wage_bill_managers(wage_bill):
    wage_bill_managers = wage_sheets.WageSheet.objects.filter(
        wage_bill=wage_bill
    ).order_by().values("field_manager_user").distinct()

    return wage_bill_managers


def get_supervisor_wage_bill_total(wage_bill, manager):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)

    supervisor_wage_total = wage_sheets.WageSheet.objects.filter(
        id__in=wage_bill_sheets, field_manager_user=manager
    ).values("supervisor_user").annotate(
        total=Sum('wage__payment')
    )

    return supervisor_wage_total


def get_manager_wage_bill_wage_sheets(wage_bill, manager):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)

    return wage_bill_sheets.filter(field_manager_user=manager, project_manager_status=True).order_by('supervisor_user')


def get_manager_wage_bill_total(wage_bill, manager):
    manager_wage_bill_wage_sheets = get_manager_wage_bill_wage_sheets(wage_bill, manager)

    total_ammount = 0

    for wage_sheet in manager_wage_bill_wage_sheets:
        total_ammount += wage_sheet.total_amount

    return total_ammount


def get_wage_bill_total_payment(wage_bill):
    wage_bill_total = wage_bills.ConsolidatedWageBillPayment.objects.filter(
        wage_bill=wage_bill
    ).aggregate(total=Sum('total_payment'))

    return wage_bill_total['total']

def get_wage_bill_activity_summary(wage_bill):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)

    wage_bill_wages = wage_sheets.Wage.objects.filter(wage_sheet__in=wage_bill_sheets,
                                                      is_pm_approved=True)
    activity_summary = wage_bill_wages.values("activity").annotate(total_qty = Sum('quantity'))

    
    return activity_summary                                                    

