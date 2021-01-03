from projects.models import Deduction
from projects.selectors.wage_sheets import get_wage_sheet

def get_all_deductions():
    return Deduction.objects.all()


def get_deductions(wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)
    return Deduction.objects.filter(wage_sheet=wage_sheet)


def get_deduction(id):
    return Deduction.objects.get(pk=id)
