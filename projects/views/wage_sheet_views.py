from projects.constants import GENERAL_MANAGER, PROJECT_MANAGER, FIELD_MANAGER
from projects.decorators.auth_decorators import supervisor_required
from projects.selectors.complaints import get_complaints, get_complaint
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse
from django.contrib import messages

from projects.forms.wage_sheet_forms import WageSheetForm, WageForm
from projects.selectors.deductions import get_deductions, get_deduction
from projects.selectors.wage_sheets import get_all_wage_sheets, get_wage_sheet, get_wages, get_wage, \
    get_submitted_wage_sheets
import projects.selectors.wage_bill_selectors as wage_bill_selectors


@supervisor_required
def manage_wage_sheets_page(request):
    wage_bill = wage_bill_selectors.get_current_wage_bill()
    wage_sheets = get_all_wage_sheets()
    form = WageSheetForm(initial={"wage_bill": wage_bill})
    if request.method == "POST":
        form = WageSheetForm(request.POST, request.FILES)
        if form.is_valid():
            wage_sheet = form.save(commit=False)
            wage_sheet.supervisor_user = request.user
            wage_sheet.save()
            messages.success(request, "Successfully added a wage sheet")
        else:
            messages.error(request, "Integrity problems while saving wage sheet")
        return HttpResponseRedirect(reverse(manage_wage_sheets_page))
    context = {
        "wagebill": "active",
        "manage_wage_sheets": "active",
        "wage_sheets": wage_sheets,
        "wage_bill": wage_bill,
        'form': form,
    }
    return render(request, "wage_sheet/manage_wage_sheets.html", context)


@supervisor_required
def edit_wage_sheet_page(request, id):
    wage_sheet = get_wage_sheet(id)
    form = WageSheetForm(instance=wage_sheet)
    if request.method == "POST":
        form = WageSheetForm(request.POST, request.FILES, instance=wage_sheet)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited a wage sheet")
        else:
            messages.error(request, "Integrity problems while saving wage sheet")
        return HttpResponseRedirect(reverse(manage_wage_sheets_page))
    context = {
        "wagebill": "active",
        "manage_wage_sheets": "active",
        "form": form,
    }
    return render(request, "wage_sheet/edit_wage_sheet.html", context)


@supervisor_required
def delete_wage_sheet(request, id):
    wage_sheet = get_wage_sheet(id)
    wage_sheet.delete()
    messages.success(request, "Successfully deleted a wage sheet")
    return HttpResponseRedirect(reverse(manage_wage_sheets_page))


@supervisor_required
def manage_wages_page(request, wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)
    wages = get_wages(wage_sheet)
    form = WageForm()
    if request.method == "POST":
        form = WageForm(request.POST, request.FILES)
        if form.is_valid():
            wage = form.save(commit=False)
            wage.wage_sheet = wage_sheet
            wage.save()
            messages.success(request, "Successfully added a wage")
        else:
            messages.error(request, "Integrity problems while saving wage ")
        return HttpResponseRedirect(reverse(manage_wages_page, args=[wage_sheet_id]))
    context = {
        "wagebill": "active",
        "manage_wage_sheets": "active",
        "wages": wages,
        "wage_sheet": wage_sheet,
        'form': form,
    }
    return render(request, "wage_sheet/manage_wages.html", context)


@supervisor_required
def edit_wage_page(request, id):
    wage = get_wage(id)
    wage_sheet = wage.wage_sheet
    form = WageForm(instance=wage)
    if request.method == "POST":
        form = WageForm(request.POST, request.FILES, instance=wage)
        if form.is_valid():
            wage = form.save(commit=False)
            wage.wage_sheet = wage_sheet
            wage.save()
            messages.success(request, "Successfully edited a wage")
        else:
            messages.error(request, "Integrity problems while saving wage")
        return HttpResponseRedirect(reverse(manage_wages_page, args=[wage_sheet.id]))
    context = {
        "wagebill": "active",
        "manage_wage_sheets": "active",
        "form": form,
    }
    return render(request, "wage_sheet/edit_wage.html", context)


def delete_wage(request, id):
    wage = get_wage(id)
    wage.delete()
    messages.success(request, "Successfully deleted a wage")
    return HttpResponseRedirect(reverse(manage_wages_page, args=[wage.wage_sheet.id]))


def submit_wage_sheet(request, wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)

    wage_sheet.is_submitted = True
    wage_sheet.save()

    messages.success(request, "Wage Sheet Submitted Successfully")
    return HttpResponseRedirect(reverse(manage_wage_sheets_page))


def view_submitted_wagesheets(request):
    wage_sheets = get_submitted_wage_sheets()
    context = {
        "wage_sheets": wage_sheets,
    }
    return render(request, "wage_sheet/submitted_wage_sheets.html", context)


def manage_submitted_sheet(request, wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)
    wages = get_wages(wage_sheet)
    complaints = get_complaints(wage_sheet_id)
    deductions = get_deductions(wage_sheet_id)
    user = request.user
    if user.user_role == FIELD_MANAGER:  # manager
        wages = wages
    elif user.user_role == PROJECT_MANAGER:  # project manager
        wages = wages.filter(is_manager_approved=True)
        complaints = complaints.filter(is_manager_approved=True)
        deductions = deductions.filter(is_manager_approved=True)
    elif user.user_role == GENERAL_MANAGER:  # GM
        wages = wages.filter(is_pm_approved=True)
        complaints = complaints.filter(is_pm_approved=True)
        deductions = deductions.filter(is_pm_approved=True)

    context = {
        "wages": wages,
        "wage_sheet": wage_sheet,
        "complaints": complaints,
        "deductions": deductions,
    }

    return render(request, "wage_sheet/manage_submitted_sheet.html", context)


def approve_reject_wagesheet(request, wagesheet_id):
    if request.method == "POST":
        wage_sheet = get_wage_sheet(wagesheet_id)
        wages = get_wages(wage_sheet)
        complaints = get_complaints(wagesheet_id)
        deductions = get_deductions(wagesheet_id)
        user = request.user
        if user.user_role == FIELD_MANAGER:
            wage_sheet.manager_comment = request.POST.get("wage_comment")
            wage_sheet.manager_status = request.POST.get("wage_action")
            wage_sheet.save()
            wages.filter(is_manager_approved=True).update(is_pm_approved=True)
            complaints.filter(is_manager_approved=True).update(is_pm_approved=True)
            deductions.filter(is_manager_approved=True).update(is_pm_approved=True)
        elif user.user_role == PROJECT_MANAGER:
            wage_sheet.project_manager_status = request.POST.get("wage_action")
            wage_sheet.project_manager_comment = request.POST.get("wage_comment")
            wage_sheet.save()
            wages.filter(is_pm_approved=True).update(is_gm_approved=True)
            complaints.filter(is_manager_approved=True).update(is_gm_approved=True)
            deductions.filter(is_manager_approved=True).update(is_gm_approved=True)
        elif user.user_role == GENERAL_MANAGER:
            wage_sheet.gm_status = request.POST.get("wage_action")
            wage_sheet.gm_comment = request.POST.get("wage_comment")
            wage_sheet.save()
        messages.success(request, "Action saved Successfully")
        return HttpResponseRedirect(reverse(manage_submitted_sheet, args=[wagesheet_id]))


def reject_wage(request, wage_id):
    wage = get_wage(wage_id)
    user = request.user
    if user.user_role == FIELD_MANAGER:
        wage.is_manager_approved = False
    elif user.user_role == PROJECT_MANAGER:
        wage.is_pm_approved = False
    elif user.user_role == GENERAL_MANAGER:
        wage.is_gm_approved = False
    try:
        wage.save()
        messages.success(request, "Wage rejected")
    except:
        messages.error(request, "Operation was no successfull")
    return HttpResponseRedirect(reverse(manage_submitted_sheet, args=[wage.wage_sheet.id]))


def reject_complaint(request, complaint_id, role):
    complaint = get_complaint(complaint_id)
    user = request.user
    if user.user_role == FIELD_MANAGER:
        complaint.is_manager_approved = False
    elif user.user_role == PROJECT_MANAGER:
        complaint.is_pm_approved = False
    elif user.user_role == FIELD_MANAGER:
        complaint.is_gm_approved = False
    try:
        complaint.save()
        messages.success(request, "Complaint rejected")
    except:
        messages.error(request, "Operation was no successfull")

    return HttpResponseRedirect(reverse(manage_submitted_sheet, args=[complaint.wage_sheet.id, role]))


def reject_deduction(request, deduction_id, role):
    deduction = get_deduction(deduction_id)
    user = request.user
    if user.user_role == FIELD_MANAGER:
        deduction.is_manager_approved = False
    elif user.user_role == PROJECT_MANAGER:
        deduction.is_pm_approved = False
    elif user.user_role == GENERAL_MANAGER:
        deduction.is_gm_approved = False
    try:
        deduction.save()

        messages.success(request, "deduction rejected")
    except:
        messages.error(request, "Operation was not successfull")

    return HttpResponseRedirect(reverse(manage_submitted_sheet, args=[deduction.wage_sheet.id, role]))
