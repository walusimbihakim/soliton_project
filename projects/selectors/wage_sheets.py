from projects.models import WageSheet, Wage


def get_all_wage_sheets():
    return WageSheet.objects.all()


def get_wage_sheet(id):
    return WageSheet.objects.get(pk=id)


def get_wages(wage_sheet):
    return Wage.objects.filter(wage_sheet=wage_sheet)


def get_wage(id):
    return Wage.objects.get(pk=id)


def get_submitted_wage_sheets():
    return WageSheet.objects.filter(is_submitted=True,)
