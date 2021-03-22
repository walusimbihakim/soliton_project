from projects.models import WageSheet, Wage


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


def get_submitted_wage_sheets():
    return WageSheet.objects.filter(is_submitted=True, )


def get_gm_wage_sheets_for_approval():
    # General manager wage sheets for approval
    return WageSheet.objects.filter(is_submitted=True, project_manager_status=True, approved=False, rejected=False)


def get_pm_wage_sheets_for_approval():
    # Project manager wage sheets for approval
    return WageSheet.objects.filter(is_submitted=True, project_manager_status=None, manager_status=True, approved=False,
                                    rejected=False)


def get_fm_wage_sheets_for_approval():
    # Field manager wage sheets for approval
    return WageSheet.objects.filter(is_submitted=True, manager_status=None, approved=False, rejected=False)
