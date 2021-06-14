from projects.models import WageSheet, Wage
from projects.models.wage_sheets import GroupWage
from projects.procedures import calculate_total_wages
from projects.selectors.wage_bill_selectors import get_current_wage_bill, get_wage_bill, \
    get_wage_bill_worker_wages_per_day, get_wage_bill_worker_complaints_per_day, get_wage_bill_worker_deductions_per_day


def get_all_wage_sheets():
    return WageSheet.objects.all()


def get_non_submitted_wage_sheets(supervisor_user):
    return WageSheet.objects.filter(supervisor_user=supervisor_user, is_submitted=False)


def get_user_submitted_wage_sheets(supervisor_user):
    # Display the most recent
    return WageSheet.objects.filter(supervisor_user=supervisor_user, is_submitted=True).order_by('-id')


def get_wage_sheet(id):
    return WageSheet.objects.get(pk=id)


def get_wages(wage_sheet):
    return Wage.objects.filter(wage_sheet=wage_sheet)


def get_wage(id):
    return Wage.objects.get(pk=id)


def get_group_wages(wage_sheet):
    return GroupWage.objects.filter(wage_sheet=wage_sheet)


def get_group_wage(id):
    return GroupWage.objects.get(pk=id)


def get_rejected_wages(wage_sheet):
    return Wage.objects.filter(wage_sheet=wage_sheet, is_manager_approved=False)


def get_approved_wages(wage_sheet):
    return Wage.objects.filter(wage_sheet=wage_sheet, is_manager_approved=True)


def get_submitted_wage_sheets():
    return WageSheet.objects.filter(is_submitted=True, )


def get_gm_wage_sheets_for_approval():
    # General manager wage sheets for approval
    return WageSheet.objects.filter(is_submitted=True, project_manager_status=True, approved=False, rejected=False)


def get_pm_wage_sheets_for_approval(project_manager_user):
    # Project manager wage sheets for approval
    return WageSheet.objects.filter(
        project_manager_user=project_manager_user,
        is_submitted=True, project_manager_status=None,
        manager_status=True, approved=False,
        rejected=False
    )


def get_fm_wage_sheets_for_approval(field_manager_user):
    # Field manager wage sheets for approval
    return WageSheet.objects.filter(field_manager_user=field_manager_user, is_submitted=True, manager_status=None,
                                    approved=False, rejected=False)


def get_current_wage_bill_wage_sheets():
    current_wage_bill = get_current_wage_bill()
    return WageSheet.objects.filter(wage_bill=current_wage_bill, is_submitted=True)


def get_submitted_wage_bill_wage_sheets(id):
    wage_bill = get_wage_bill(id)
    return WageSheet.objects.filter(wage_bill=wage_bill, is_submitted=True)


def get_worker_payment_per_day(wage_bill, worker, date):
    wages = get_wage_bill_worker_wages_per_day(wage_bill, worker, date)  # Returns 0
    complaints = get_wage_bill_worker_complaints_per_day(wage_bill, worker, date)  # Returns 0
    deductions = get_wage_bill_worker_deductions_per_day(wage_bill, worker, date)  # Returns 0
    total_wages = calculate_total_wages(wages)
    total_complaints = calculate_total_wages(complaints)
    total_deductions = calculate_total_wages(deductions)
    return (total_wages + total_complaints) - total_deductions
