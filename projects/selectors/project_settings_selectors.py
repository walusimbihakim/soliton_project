from projects.models.project_settings import UnitOfMeasure
from projects.models.budget import Expense

def get_measures():
    return UnitOfMeasure.objects.all()

def get_expenses():
    return Expense.objects.all()

def get_expense(expense_id):
    return Expense.objects.get(pk=expense_id)
