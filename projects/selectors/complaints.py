from django.db.models.aggregates import Sum
from projects.models import Complaint
from projects.selectors.wage_sheets import get_wage_sheet
from projects.selectors.wage_bill_selectors import get_wage_bill_sheets

def get_all_complaints():
    return Complaint.objects.all()


def get_complaints(wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)
    return Complaint.objects.filter(wage_sheet=wage_sheet)


def get_complaint(id):
    return Complaint.objects.get(pk=id)



def get_worker_complaints(worker, wage_bill):
    wage_bill_sheets = get_wage_bill_sheets(wage_bill)

    wage_sheet_complaints = Complaint.objects.filter(
            wage_sheet__in=wage_bill_sheets, 
            is_gm_approved=True, 
            worker=worker
            )

    return wage_sheet_complaints.aggregate(payment=Sum("payment"))


