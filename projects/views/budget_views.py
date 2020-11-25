from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from projects.selectors.pip_selectors import get_pip
from projects.selectors.budget_selectors import (
    get_budget, 
    get_material_budgets, 
    get_material_budget,
    get_execution_budgets,
    get_execution_budget, 
    get_expense_budgets,
    get_expense_budget,
    get_expense,
)
from projects.services.budget_services import create_pip_budget
from projects.forms.budget_forms import MaterialBudgetForm, ExecutionBudgetForm, ExpenseBudgetForm

from projects.selectors.material_selectors import get_material
from clients.selectors import get_client_activity_rate


def manage_budgets_view(request, budget_id):
    budget = get_budget(budget_id)

    client_id = budget.pip.scope.survey.project.client_id
    activity_id = budget.pip.activity_id

    activity_client_rate = get_client_activity_rate(client_id, activity_id)

    material_budget_form = MaterialBudgetForm(initial={"budget":budget})
    execution_budget_form = ExecutionBudgetForm(
        initial={
            "budget": budget, 
            "quantity": budget.pip.scope.quantity,
            "unit_cost": activity_client_rate.rate,
            "total_cost": (activity_client_rate.rate*budget.pip.scope.quantity)
            }
        )
    expense_budget_form = ExpenseBudgetForm(initial={"budget":budget}) 

    material_budgets = get_material_budgets(budget)
    execution_budgets = get_execution_budgets(budget)
    expense_budgets = get_expense_budgets(budget)
        

    context ={
        "budget": budget,
        "material_budgets": material_budgets,
        "execution_budgets": execution_budgets,
        "expense_budgets": expense_budgets,
        "expense_budget_form": expense_budget_form,
        "execution_budget_form": execution_budget_form,
        "material_budget_form": material_budget_form
    }
    return render(request, "budget/manage_budgets.html", context)

def create_budget(request,pip_id):
    pip = get_pip(pip_id)

    budget = create_pip_budget(pip)

    return HttpResponseRedirect(reverse(manage_budgets_view, args=[pip.budget.id]))

def add_material_budget_view(request, budget_id):

    if request.method == "POST":
        material_budget_form = MaterialBudgetForm(request.POST)

        if material_budget_form.is_valid():
            material_budget_form.save()

            messages.success(request, 'Budget Record added successfully')
        
        else:
            messages.warning(request, 'Record Not Saved, Check your inputs and try again')
    
    return HttpResponseRedirect(reverse(manage_budgets_view, args=[budget_id]))

def edit_material_budget_view(request, budget_id):
    material_budget = get_material_budget(budget_id)

    material_edit_form = MaterialBudgetForm(instance=material_budget)

    if request.method == "POST":
        material_edit_form = MaterialBudgetForm(request.POST, instance=material_budget)

        if material_edit_form.is_valid():
            material_edit_form.save()

            messages.success(request, 'Changes Saved successfully')

            return HttpResponseRedirect(reverse(manage_budgets_view, args=[material_budget.budget_id]))
        
        else:
            messages.warning(request, 'Somthing Went, Check your Inputs and Try Again')

            return HttpResponseRedirect(reverse(manage_budgets_view, args=[material_budget.budget_id]))

    context = {
        "budget_edit_form": material_edit_form,

    }

    return render(request, "budget/edit_budget.html", context)

def  delete_material_budget_view(request, budget_id):
    budget_record = get_material_budget(budget_id)

    budget_record.delete()

    messages.success(request, 'Record Deleted successfully')

    return HttpResponseRedirect(reverse(manage_budgets_view, args=[budget_record.budget_id]))


def add_execution_budget_view(request, budget_id):

    if request.method == "POST":
        execution_budget_form = ExecutionBudgetForm(request.POST)

        if execution_budget_form.is_valid():
            execution_budget_form.save()

            messages.danger(request, 'Budget Record added successfully')
        
        else:
            messages.warning(request, 'Record Not Saved, Check your inputs and try again')
    
    return HttpResponseRedirect(reverse(manage_budgets_view, args=[budget_id]))

def edit_execution_budget_view(request, budget_id):
    execution_budget = get_execution_budget(budget_id)

    execution_edit_form = ExecutionBudgetForm(instance=execution_budget)

    if request.method == "POST":
        execution_edit_form = ExecutionBudgetForm(request.POST, instance=execution_budget)

        if execution_edit_form.is_valid():
            execution_edit_form.save()

            messages.success(request, 'Changes Saved successfully')

            return HttpResponseRedirect(reverse(manage_budgets_view, args=[execution_budget.budget_id]))
        
        else:
            messages.Warning(request, 'Somthing Went, Check your Inputs and Try Again')

            return HttpResponseRedirect(reverse(manage_budgets_view, args=[execution_budget.budget_id]))

    context = {
        "budget_edit_form": execution_edit_form,

    }

    return render(request, "budget/edit_budget.html", context)

def  delete_execution_budget_view(request, budget_id):
    budget_record = get_execution_budget(budget_id)

    budget_record.delete()

    messages.success(request, 'Record Deleted successfully')

    return HttpResponseRedirect(reverse(manage_budgets_view, args=[budget_record.budget_id]))


def add_expense_budget_view(request, budget_id):

    if request.method == "POST":
        expense_budget_form = ExpenseBudgetForm(request.POST)

        if expense_budget_form.is_valid():
            expense_budget_form.save()

            messages.danger(request, 'Budget Record added successfully')
        
        else:
            messages.warning(request, 'Record Not Saved, Check your inputs and try again')
    
    return HttpResponseRedirect(reverse(manage_budgets_view, args=[budget_id]))

def edit_expense_budget_view(request, budget_id):
    expense_budget = get_expense_budget(budget_id)

    expense_edit_form = ExpenseBudgetForm(instance=expense_budget)

    if request.method == "POST":
        expense_edit_form = ExpenseBudgetForm(request.POST, instance=expense_budget)

        if expense_edit_form.is_valid():
            expense_edit_form.save()

            messages.success(request, 'Changes Saved successfully')

            return HttpResponseRedirect(reverse(manage_budgets_view, args=[expense_budget.budget_id]))
        
        else:
            messages.Warning(request, 'Somthing Went, Check your Inputs and Try Again')

            return HttpResponseRedirect(reverse(manage_budgets_view, args=[expense_budget.budget_id]))

    context = {
        "budget_edit_form": expense_edit_form,
    }

    return render(request, "budget/edit_budget.html", context)

def  delete_expense_budget_view(request, budget_id):
    budget_record = get_expense_budget(budget_id)

    budget_record.delete()

    messages.success(request, 'Record Deleted successfully')

    return HttpResponseRedirect(reverse(manage_budgets_view, args=[budget_record.budget_id]))

def get_material_unitcost_view(request):
    material_id = request.GET['material']

    material = get_material(material_id)

    material_unitcost = material.unit_cost

    return JsonResponse({'success': True, 'unit_cost': material_unitcost})

def get_expense_rate_view(request):
    print("Am here")
    expense_id = request.GET['expense']

    expense = get_expense(expense_id)

    expense_rate = expense.rate

    return JsonResponse({'success': True, 'rate': expense_rate})
