from django.utils import timezone
from projects.models import WageSheet


def unsubmit_wage_sheet(wage_sheet):
    wage_sheet.approved = False
    wage_sheet.rejected = False
    wage_sheet.gm_status = None
    wage_sheet.gm_comment = ""
    wage_sheet.manager_status = None
    wage_sheet.manager_comment = ""
    wage_sheet.project_manager_status = None
    wage_sheet.project_manager_comment = ""
    wage_sheet.is_submitted = False
    wage_sheet.save()


def reset_payment_approvals(wage_sheet):
    wages = wage_sheet.wage_set.all()
    complaints = wage_sheet.complaint_set.all()
    deductions = wage_sheet.deduction_set.all()
    wages.update(
        is_manager_approved=True,
        is_pm_approved=None,
        is_gm_approved=None,
        is_payed=None
    )
    complaints.update(
        is_manager_approved=True,
        is_pm_approved=None,
        is_gm_approved=None,
        is_payed=None
    )
    deductions.update(
        is_manager_approved=True,
        is_pm_approved=None,
        is_gm_approved=None,
        is_payed=None
    )


def retract(wage_sheet: WageSheet):
    unsubmit_wage_sheet(wage_sheet)
    reset_payment_approvals(wage_sheet)


def submit_wage_sheet_service(wage_sheet):
    wage_sheet.is_submitted = True
    wage_sheet.supervisor_submission_time = timezone.now()
    wage_sheet.save()


def approve_or_reject_wage_sheet_by_field_manager(is_approved, wage_sheet, comment):
    wage_sheet.manager_comment = comment
    wage_sheet.manager_status = is_approved
    wage_sheet.field_manager_approval_time = timezone.now()
    wage_sheet.save()


def approve_or_reject_wage_sheet_by_project_manager(is_approved, wage_sheet, comment):
    wage_sheet.project_manager_status = is_approved
    wage_sheet.project_manager_comment = comment
    wage_sheet.project_manager_approval_time = timezone.now()
    wage_sheet.approved = True
    wage_sheet.save()


def approve_or_reject_payments_by_fieldmanager(is_wage_sheet_approved, wages, complaints, deductions):
    if is_wage_sheet_approved:
        wages.filter(is_manager_approved=True).update(is_pm_approved=True)
        complaints.filter(is_manager_approved=True).update(is_pm_approved=True)
        deductions.filter(is_manager_approved=True).update(is_pm_approved=True)
    else:
        wages.filter(is_manager_approved=True).update(is_pm_approved=False)
        complaints.filter(is_manager_approved=True).update(is_pm_approved=False)
        deductions.filter(is_manager_approved=True).update(is_pm_approved=False)


def approve_or_reject_payments_by_project_manager(is_wage_sheet_approved, wages, complaints, deductions):
    if is_wage_sheet_approved:
        wages.filter(is_pm_approved=True).update(is_gm_approved=True)
        complaints.filter(is_manager_approved=True).update(is_gm_approved=True)
        deductions.filter(is_manager_approved=True).update(is_gm_approved=True)
    else:
        wages.filter(is_pm_approved=True).update(is_gm_approved=False)
        wages.filter(is_pm_approved=True).update(is_gm_approved=False)
        wages.filter(is_pm_approved=True).update(is_gm_approved=False)
