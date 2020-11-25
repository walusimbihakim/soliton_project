from projects.models import WageSheet, Wage


def get_all_wage_sheets():
    return WageSheet.objects.all()


def get_wage_sheet(id):
    return WageSheet.objects.get(pk=id)


def get_wages(wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)
    return Wage.objects.filter(wage_sheet=wage_sheet)


def get_wage(id):
    return Wage.objects.get(pk=id)
