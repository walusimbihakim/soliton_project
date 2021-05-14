from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse
from django.contrib import messages

from projects.constants import INTEGRITY_ERROR_MESSAGE, INVALID_FORM_MESSAGE
from projects.selectors.wage_sheets import get_wage_sheet
from projects.selectors.deductions import get_deductions, get_deduction
from projects.forms.deduction_forms import DeductionForm


def manage_deductions_page(request, wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)
    deductions = get_deductions(wage_sheet_id)
    form = DeductionForm()
    if request.method == "POST":
        form = DeductionForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                deduction = form.save(commit=False)
                deduction.wage_sheet = wage_sheet
                deduction.save()
                messages.success(request, "Successfully added a deduction")
            except IntegrityError:
                messages.error(request, INTEGRITY_ERROR_MESSAGE)
        else:
            messages.error(request, INVALID_FORM_MESSAGE)
        return HttpResponseRedirect(reverse(manage_deductions_page, args=[wage_sheet_id]))
    context = {
        "wagebill": "active",
        "manage_wage_sheets": "active",
        "deductions": deductions,
        "wage_sheet":wage_sheet,
        'form': form,
    }
    return render(request, "wage_sheet/manage_deductions.html", context)


def edit_deduction_page(request, id):
    deduction = get_deduction(id)
    wage_sheet = deduction.wage_sheet
    form = DeductionForm(instance=deduction)
    if request.method == "POST":
        form = DeductionForm(request.POST, request.FILES, instance=deduction)
        if form.is_valid():
            try:
                deduction = form.save(commit=False)
                deduction.wage_sheet = wage_sheet
                deduction.save()
                messages.success(request, "Successfully edited a deduction")
            except IntegrityError:
                messages.error(request, INTEGRITY_ERROR_MESSAGE)
        else:
            messages.error(request, INVALID_FORM_MESSAGE)
        return HttpResponseRedirect(reverse(manage_deductions_page, args=[wage_sheet.id]))
    context = {
        "wagebill": "active",
        "manage_wage_sheets": "active",
        "form": form,
    }
    return render(request, "wage_sheet/edit_deduction.html", context)


def delete_deduction(request, id):
    deduction = get_deduction(id)
    deduction.delete()
    messages.success(request, "Successfully deleted a deduction")
    return HttpResponseRedirect(reverse(manage_deductions_page,
                                        args=[deduction.wage_sheet.id]))
