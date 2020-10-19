from projects.models.budget import (
    Budget, 
    MaterialBudget, 
    ExecutionBudget, 
    ExpenseBudget,
    Expense,
)

def get_budget(budget_id):
    return Budget.objects.get(pk=budget_id)

def get_material_budgets(budget):
    return MaterialBudget.objects.filter(budget=budget.id)

def get_execution_budgets(budget):
    return ExecutionBudget.objects.filter(budget=budget)

def get_expense_budgets(budget):
    return ExpenseBudget.objects.filter(budget=budget)

def  get_material_budget(budget_id):
    return MaterialBudget.objects.get(pk=budget_id)

def  get_execution_budget(budget_id):
    return ExecutionBudget.objects.get(pk=budget_id)

def  get_expense_budget(budget_id):
    return ExpenseBudget.objects.get(pk=budget_id)

def get_expense(expense_id):
    return Expense.objects.get(pk=expense_id)