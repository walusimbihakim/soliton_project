from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse

from projects.models import UnitOfMeasure
from projects.forms.project_settings_forms import UnitOfMeasureForm, ExpenseForm
from projects.selectors.project_settings_selectors import get_measures, get_expenses, get_expense

def unit_of_measure_view(request):
    unit_form = UnitOfMeasureForm()

    if request.method == "POST":
        unit_form = UnitOfMeasureForm(request.POST)

        if unit_form.is_valid():
            unit_form.save()

            messages.success(request, 'Unit Measure added Successfully')

    units_of_measures = get_measures()

    context = {
        "unit_form": unit_form,
        "units": units_of_measures
    }

    return render(request, "project_settings/uom.html", context)

def manage_expense_view(request):
    expense_form = ExpenseForm()

    if request.method == "POST":
        expense_form = ExpenseForm(request.POST)

        if expense_form.is_valid():
            expense_form.save()

            messages.success(request, 'Expense Record added Successfully')

        else:
            messages.success(request, 'One or More input value(s) are not in correct format, Check your inputs and try again')
    
    expenses = get_expenses()

    context = {
        "expenses": expenses,
        "expense_form": expense_form,
    }

    return render(request, "project_settings/manage_expenses.html", context)

def edit_expense_view(request, expense_id):
    expense = get_expense(expense_id)

    expense_form = ExpenseForm(instance=expense)

    if request.method == "POST":
        expense_form = ExpenseForm(request.POST, instance=expense)

        if expense_form.is_valid():
            expense_form.save()

            messages.success(request, 'Changes to the expense Record Saved Successfully')

            return HttpResponseRedirect(reverse(manage_expense_view))

        else:
            messages.success(request, 'One or More input value(s) are not in correct format, Check your inputs and try again')

            return HttpResponseRedirect(reverse(manage_expense_view))

    expenses = get_expenses()

    context = {
        "expense": expense,
        "expenses": expenses,
        "expense_form": expense_form,
    }

    return render(request, "project_settings/edit_expense.html", context)

def delete_expense(request, expense_id):
    expense = get_expense(expense_id)

    expense.delete()

    messages.success(request, 'Expense Record Deleted Successfully')

    return HttpResponseRedirect(reverse(manage_expense_view))

