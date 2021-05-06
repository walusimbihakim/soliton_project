from django.db import IntegrityError

from projects.constants import GENERAL_MANAGER, PROJECT_MANAGER, FIELD_MANAGER
from projects.decorators.auth_decorators import supervisor_required
from projects.selectors.complaints import get_complaints, get_complaint
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.urls import reverse
from django.contrib import messages

from projects.forms.wage_sheet_forms import WageSheetForm, WageForm, GroupWageForm
from projects.selectors.deductions import get_deductions, get_deduction
from projects.selectors.wage_sheets import get_wage_sheet, get_wages, get_wage, \
    get_fm_wage_sheets_for_approval, get_pm_wage_sheets_for_approval, \
    get_gm_wage_sheets_for_approval, get_non_submitted_wage_sheets, \
    get_user_submitted_wage_sheets, get_rejected_wages, get_approved_wages, get_current_wage_bill_wage_sheets, \
    get_submitted_wage_bill_wage_sheets, get_group_wages, get_group_wage
import projects.selectors.wage_bill_selectors as wage_bill_selectors
from projects.services.wage_sheet_services import retract


def manage_wage_sheets_page(request):
    wage_bill = wage_bill_selectors.get_current_wage_bill()
    wage_sheets = get_non_submitted_wage_sheets(request.user)
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
        "wage_sheets_page": "active",
        "manage_wage_sheets": "active",
        "wage_sheets": wage_sheets,
        "wage_bill": wage_bill,
        'form': form,
    }
    return render(request, "wage_sheet/manage_wage_sheets.html", context)


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
        "wage_sheets_page": "active",
        "manage_wage_sheets": "active",
        "form": form,
    }
    return render(request, "wage_sheet/edit_wage_sheet.html", context)


def user_submitted_wage_sheets_page(request):
    wage_sheets = get_user_submitted_wage_sheets(request.user)
    context = {
        "wage_sheets_page": "active",
        "wage_sheets": wage_sheets,
    }
    return render(request, "wage_sheet/user_submitted_wage_sheets.html", context)


def submitted_wage_sheet_page(request, id):
    wage_sheet = get_wage_sheet(id)
    approved_wages = get_approved_wages(wage_sheet)
    rejected_wages = get_rejected_wages(wage_sheet)
    complaints = get_complaints(id)
    deductions = get_deductions(id)
    context = {
        "wage_sheets_page": "active",
        "wage_sheet": wage_sheet,
        "wages": approved_wages,
        "rejected_wages": rejected_wages,
        "complaints": complaints,
        "deductions": deductions
    }
    return render(request, "wage_sheet/submitted_wage_sheet.html", context)


def current_wage_bill_sheets_page(request):
    wage_sheets = get_current_wage_bill_wage_sheets()
    wage_bill = wage_bill_selectors.get_current_wage_bill()
    context = {
        "current_wage_bill_sheets": "active",
        "wage_sheets": wage_sheets,
        "wage_bill": wage_bill
    }
    return render(request, "wage_sheet/wage_bill_sheets.html", context)


def wage_bill_sheets_page(request, wage_bill_id):
    wage_sheets = get_submitted_wage_bill_wage_sheets(wage_bill_id)
    wage_bill = wage_bill_selectors.get_wage_bill(wage_bill_id)
    context = {
        "view_all_wage_sheets": "active",
        "wage_sheets": wage_sheets,
        "wage_bill": wage_bill
    }
    return render(request, "wage_sheet/wage_bill_sheets.html", context)


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
    form = WageForm(user=request.user)
    if request.method == "POST":
        form = WageForm(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            wage = form.save(commit=False)
            wage.wage_sheet = wage_sheet
            wage.save()
            messages.success(request, "Successfully added a wage")
        else:
            messages.error(request, "Integrity problems while saving wage ")
        return HttpResponseRedirect(reverse(manage_wages_page, args=[wage_sheet_id]))
    context = {
        "wage_sheets_page": "active",
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
    form = WageForm(user=request.user, instance=wage)
    if request.method == "POST":
        form = WageForm(user=request.user, data=request.POST, files=request.FILES, instance=wage)
        if form.is_valid():
            wage = form.save(commit=False)
            wage.wage_sheet = wage_sheet
            wage.save()
            messages.success(request, "Successfully edited a wage")
        else:
            messages.error(request, "Integrity problems while saving wage")
        return HttpResponseRedirect(reverse(manage_wages_page, args=[wage_sheet.id]))
    context = {
        "wage_sheets_page": "active",
        "manage_wage_sheets": "active",
        "form": form,
    }
    return render(request, "wage_sheet/edit_wage.html", context)


def delete_wage(request, id):
    wage = get_wage(id)
    wage.delete()
    messages.success(request, "Successfully deleted a wage")
    return HttpResponseRedirect(reverse(manage_wages_page, args=[wage.wage_sheet.id]))


@supervisor_required
def manage_group_wages_page(request, wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)
    group_wages = get_group_wages(wage_sheet)
    form = GroupWageForm(user=request.user)
    if request.method == "POST":
        form = GroupWageForm(user=request.user, data=request.POST)
        if form.is_valid():
            group_wage = form.save(commit=False)
            group_wage.wage_sheet = wage_sheet
            try:
                group_wage.save()
                messages.success(request, "Successfully added a group wage")
            except IntegrityError:
                messages.error(request, "You tried to enter a duplicate record")
        else:
            messages.error(request, "Incomplete or Invalid form")
        return HttpResponseRedirect(reverse(manage_group_wages_page, args=[wage_sheet_id]))
    context = {
        "wage_sheets_page": "active",
        "manage_wage_sheets": "active",
        "group_wages": group_wages,
        "wage_sheet": wage_sheet,
        'form': form,
    }
    return render(request, "wage_sheet/manage_group_wages.html", context)


@supervisor_required
def edit_group_wage_page(request, id):
    group_wage = get_group_wage(id)
    wage_sheet = group_wage.wage_sheet
    form = GroupWageForm(user=request.user, instance=group_wage)
    if request.method == "POST":
        form = GroupWageForm(user=request.user, data=request.POST, instance=group_wage)
        if form.is_valid():
            group_wage = form.save(commit=False)
            group_wage.wage_sheet = wage_sheet
            group_wage.save()
            messages.success(request, "Successfully edited a group wage")
        else:
            messages.error(request, "Integrity problems while saving group wage")
        return HttpResponseRedirect(reverse(manage_group_wages_page, args=[wage_sheet.id]))
    context = {
        "wage_sheets_page": "active",
        "manage_wage_sheets": "active",
        "form": form,
    }
    return render(request, "wage_sheet/edit_group_wage.html", context)


def delete_wage_group(request, id):
    group_wage = get_group_wage(id)
    group_wage.delete()
    messages.success(request, "Successfully deleted a group wage")
    return HttpResponseRedirect(reverse(manage_group_wages_page, args=[group_wage.wage_sheet.id]))


def submit_wage_sheet(request, wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)

    wage_sheet.is_submitted = True
    wage_sheet.save()

    messages.success(request, "Wage Sheet Submitted Successfully")
    return HttpResponseRedirect(reverse(manage_wage_sheets_page))


@supervisor_required
def retract_wage_sheet(request, wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)
    if not wage_sheet.approved:
        retract(wage_sheet)
        messages.success(request, "Wage Sheet retracted Successfully")
        return HttpResponseRedirect(reverse(manage_wage_sheets_page))
    messages.error(request, "Wage Sheet is already approved")


def approve_or_reject_wagesheets(request):
    wage_sheets = None
    user = request.user
    if user.user_role == FIELD_MANAGER:
        wage_sheets = get_fm_wage_sheets_for_approval(user)
    elif user.user_role == PROJECT_MANAGER:
        wage_sheets = get_pm_wage_sheets_for_approval()
    elif user.user_role == GENERAL_MANAGER:
        wage_sheets = get_gm_wage_sheets_for_approval()
    context = {
        "wage_sheets_page": "active",
        "wage_sheets": wage_sheets,
    }
    return render(request, "wage_sheet/approve_or_reject_wage_sheets.html", context)


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
        "wage_sheets_page": "active",
        "wages": wages,
        "wage_sheet": wage_sheet,
        "complaints": complaints,
        "deductions": deductions,
    }

    return render(request, "wage_sheet/manage_submitted_sheet.html", context)


def approve_reject_wage_sheets_page(request, wagesheet_id):
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
            wage_sheet.approved = True
            wage_sheet.save()
        messages.success(request, "Action saved Successfully")
        return HttpResponseRedirect(reverse(approve_or_reject_wagesheets))


def reject_wage(request):
    wage_id = request.POST['id_wage']

    wage = get_wage(wage_id)
    user = request.user

    if user.user_role == FIELD_MANAGER:
        wage.is_manager_approved = False
    elif user.user_role == PROJECT_MANAGER:
        wage.is_pm_approved = False
    elif user.user_role == GENERAL_MANAGER:
        wage.is_gm_approved = False
    try:
        wage.remarks = request.POST.get('reject_comment')
        wage.save()
        messages.success(request, "Wage rejected")
    except:
        messages.error(request, "Operation was no successfull")
    return HttpResponseRedirect(reverse(manage_submitted_sheet, args=[wage.wage_sheet.id]))


def reject_complaint(request):
    complaint_id = request.POST.get('id_complaint')
    complaint = get_complaint(complaint_id)
    user = request.user
    if user.user_role == FIELD_MANAGER:
        complaint.is_manager_approved = False
    elif user.user_role == PROJECT_MANAGER:
        complaint.is_pm_approved = False
    elif user.user_role == FIELD_MANAGER:
        complaint.is_gm_approved = False
    try:
        complaint.remarks = request.POST.get('reject_complaint_txt')
        complaint.save()
        messages.success(request, "Complaint rejected")
    except:
        messages.error(request, "Operation was no successfull")

    return HttpResponseRedirect(reverse(manage_submitted_sheet, args=[complaint.wage_sheet.id]))


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
