from django.db import IntegrityError
from django.db.models import Q

from project_manager.settings import BASE_DIR
from projects.constants import GENERAL_MANAGER, PROJECT_MANAGER, FIELD_MANAGER, INVALID_FORM_MESSAGE, \
    INTEGRITY_ERROR_MESSAGE
from projects.decorators.auth_decorators import supervisor_required
from projects.models import Worker, WageSheet
from projects.procedures import is_date_between, render_to_pdf
from projects.selectors.complaints import get_complaints, get_complaint
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.forms.models import model_to_dict

from projects.forms.wage_sheet_forms import WageSheetForm, WageForm, GroupWageForm, WageFromPhoneNumberForm
from projects.selectors.deductions import get_deductions, get_deduction
from projects.selectors.wage_sheets import get_wage_sheet, get_wages, get_wage, \
    get_fm_wage_sheets_for_approval, get_pm_wage_sheets_for_approval, \
    get_gm_wage_sheets_for_approval, get_non_submitted_wage_sheets, \
    get_user_submitted_wage_sheets, get_rejected_wages, get_approved_wages, get_current_wage_bill_wage_sheets, \
    get_submitted_wage_bill_wage_sheets, get_group_wages, get_group_wage
import projects.selectors.wage_bill_selectors as wage_bill_selectors
from projects.services.wage_sheet_services import retract, approve_or_reject_payments_by_fieldmanager, \
    approve_or_reject_payments_by_project_manager, approve_or_reject_wage_sheet_by_field_manager, \
    approve_or_reject_wage_sheet_by_project_manager, submit_wage_sheet_service
import projects.selectors.workers as worker_selectors
from projects.services.worker_services import create_worker_transfer
from projects.tasks.random import wage_sheet_approver_notify


def manage_wage_sheets_page(request):
    wage_bill = wage_bill_selectors.get_current_wage_bill()
    wage_sheets = get_non_submitted_wage_sheets(request.user)
    form = WageSheetForm(initial={"wage_bill": wage_bill})
    if request.method == "POST":
        form = WageSheetForm(request.POST, request.FILES)
        if form.is_valid():
            wage_sheet = form.save(commit=False)
            wage_sheet.supervisor_user = request.user
            if is_date_between(wage_sheet.date, wage_bill.start_date, wage_bill.end_date):
                try:
                    wage_sheet.save()
                    messages.success(request, "Successfully added a wage sheet")
                except IntegrityError:
                    messages.error(request, INTEGRITY_ERROR_MESSAGE)
            else:
                messages.error(request, "Wage sheet date is later or earlier than the current wage bill period. "
                                        f"Please put a wage sheet date between {wage_bill}")
        else:
            messages.error(request, INVALID_FORM_MESSAGE)
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
            try:
                form.save()
                messages.success(request, "Successfully edited a wage sheet")
            except IntegrityError:
                messages.error(request, INTEGRITY_ERROR_MESSAGE)
        else:
            messages.error(request, INVALID_FORM_MESSAGE)
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


def approved_wage_sheets_page(request):
    wage_sheets = WageSheet.objects.filter(
        Q(field_manager_user=request.user, manager_status=True) |
        Q(project_manager_user=request.user, project_manager_status=True)
    ).order_by("-id")
    context = {
        "wage_sheets": wage_sheets,
        "wage_sheets_page": "active",
    }
    return render(request, "wage_sheet/approved_wage_sheets.html", context)


def expired_wage_sheets_page(request):
    wage_sheets = WageSheet.objects.filter(
        Q(field_manager_user=request.user, is_expired=True) |
        Q(project_manager_user=request.user, is_expired=True)
    ).order_by("-id")
    context = {
        "wage_sheets": wage_sheets,
        "wage_sheets_page": "active",
    }
    return render(request, "wage_sheet/expired_wage_sheets.html", context)


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
    wage_from_phone_number_form = WageFromPhoneNumberForm(user=request.user)
    if request.method == "POST":
        form = WageForm(user=request.user, data=request.POST)
        if form.is_valid():
            try:
                wage = form.save(commit=False)
                wage.wage_sheet = wage_sheet
                wage.save()
                messages.success(request, "Successfully added a wage")
            except IntegrityError:
                messages.error(request, INTEGRITY_ERROR_MESSAGE)
        else:
            messages.error(request, INVALID_FORM_MESSAGE)
        return HttpResponseRedirect(reverse(manage_wages_page, args=[wage_sheet_id]))
    context = {
        "wage_sheets_page": "active",
        "manage_wage_sheets": "active",
        "wages": wages,
        "wage_sheet": wage_sheet,
        'form': form,
        "wage_from_phone_number_form": wage_from_phone_number_form
    }
    return render(request, "wage_sheet/manage_wages.html", context)


@supervisor_required
def edit_wage_page(request, id):
    wage = get_wage(id)
    wage_sheet = wage.wage_sheet
    form = WageForm(user=request.user, instance=wage)
    if request.method == "POST":
        form = WageForm(user=request.user, data=request.POST, instance=wage)
        if form.is_valid():
            try:
                wage = form.save(commit=False)
                wage.wage_sheet = wage_sheet
                wage.save()
                messages.success(request, "Successfully edited a wage")
            except IntegrityError:
                messages.error(request, INTEGRITY_ERROR_MESSAGE)
        else:
            messages.error(request, INVALID_FORM_MESSAGE)
        return HttpResponseRedirect(reverse(manage_wages_page, args=[wage_sheet.id]))
    context = {
        "wage_sheets_page": "active",
        "manage_wage_sheets": "active",
        "form": form,
    }
    return render(request, "wage_sheet/edit_wage.html", context)


def add_wage_from_phone_number_page(request, wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)
    
    if request.method == "POST":
        form = WageFromPhoneNumberForm(user=request.user, data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            try:
                worker = Worker.objects.get(mobile_money_number=phone_number)
            except Worker.DoesNotExist:
                messages.error(request, f"Worker with phone number {phone_number} does not exist")
                return HttpResponseRedirect(reverse(manage_wages_page, args=[wage_sheet_id]))
            try:
                wage = form.save(commit=False)
                wage.wage_sheet = wage_sheet
                wage.worker = worker
                wage.save()
                create_worker_transfer(worker, request.user)
                messages.success(request, "Successfully added a wage")
            except IntegrityError:
                messages.error(request, INTEGRITY_ERROR_MESSAGE)
        else:
            messages.error(request, INVALID_FORM_MESSAGE)
        return HttpResponseRedirect(reverse(manage_wages_page, args=[wage_sheet_id]))
    

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
    wage_sheet: WageSheet = get_wage_sheet(wage_sheet_id)
    submit_wage_sheet_service(wage_sheet)
    field_manager_user = wage_sheet.field_manager_user
    wage_sheet_approver_notify.delay(field_manager_user.id, wage_sheet_id)
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


def approve_or_reject_wagesheets_page(request):
    wage_sheets = None
    user = request.user
    if user.user_role == FIELD_MANAGER:
        wage_sheets = get_fm_wage_sheets_for_approval(user)
    elif user.user_role == PROJECT_MANAGER:
        wage_sheets = get_pm_wage_sheets_for_approval(user)
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


def approve_or_reject_wage_sheets_process(request, wagesheet_id):
    if request.method == "POST":
        wage_sheet: WageSheet = get_wage_sheet(wagesheet_id)
        wages = get_wages(wage_sheet)
        complaints = get_complaints(wagesheet_id)
        deductions = get_deductions(wagesheet_id)
        user = request.user
        is_approved = request.POST.get("wage_action")
        comment = request.POST.get("wage_comment")
        if user.user_role == FIELD_MANAGER:
            approve_or_reject_wage_sheet_by_field_manager(is_approved, wage_sheet, comment)
            approve_or_reject_payments_by_fieldmanager(is_approved, wages, complaints, deductions)
            wage_sheet_approver_notify.delay(wage_sheet.project_manager_user.id, wagesheet_id)
        elif user.user_role == PROJECT_MANAGER:
            approve_or_reject_wage_sheet_by_project_manager(is_approved, wage_sheet, comment)
            approve_or_reject_payments_by_project_manager(is_approved, wages, complaints, deductions)
        messages.success(request, "Action saved Successfully")
        return HttpResponseRedirect(reverse(approve_or_reject_wagesheets_page))


def wage_sheet_pdf(self, wage_sheet_id):
    wage_sheet = get_wage_sheet(wage_sheet_id)
    wages = wage_sheet.wage_set.all()
    complaints = wage_sheet.complaint_set.all()
    deductions = wage_sheet.deduction_set.all()
    context = {
        "wage_sheet": wage_sheet,
        "base_dir": BASE_DIR,
        "wages": wages,
        "complaints": complaints,
        "deductions": deductions
    }
    pdf = render_to_pdf('pdfs/wage_sheet.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


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


def toggle_worker_list_view(request):
    option = request.GET.get('option')

    user = request.user
    worker_list = ""

    if option == 1:
        worker_list = worker_selectors.get_all_workers_registered_by(user)
    else:
        worker_list = worker_selectors.get_all_workers()

    return JsonResponse({'success': True, 'worker_list': model_to_dict(worker_list)})
