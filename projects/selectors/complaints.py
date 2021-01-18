from projects.models import Complaint
from projects.selectors.wage_sheets import get_wage_sheet

def get_all_complaints():
    return Complaint.objects.all()


def get_complaints(wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)
    return Complaint.objects.filter(wage_sheet=wage_sheet)


def get_complaint(id):
    return Complaint.objects.get(pk=id)
