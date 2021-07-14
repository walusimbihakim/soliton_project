import datetime
from datetime import date
from celery import shared_task
from django.db import IntegrityError
from twilio.base.exceptions import TwilioRestException

from project_manager.celery import app
from projects.classes.mails import WageBillCreatedMail, WageSheetsSubmissionReminder, WageSheetApprovalNotification
from projects.classes.sms_notification import SMSNotification
from projects.models import WageBill, Notification, WageSheet
from projects.selectors import wage_bill_selectors
from projects.selectors.user_selectors import get_users, get_supervisors, get_user_by_id
from projects.selectors.wage_bill_selectors import get_current_wage_bill
from projects.selectors.wage_sheets import get_wage_sheet


@app.task
def create_wage_bill():
    current_wage_bill = wage_bill_selectors.get_current_wage_bill()
    if current_wage_bill:
        current_wage_bill.status = "Done"
        current_wage_bill.save()
    current_date = date.today()
    end_date = current_date + datetime.timedelta(days=6)
    try:
        WageBill.objects.create(start_date=current_date, end_date=end_date)
    except IntegrityError as e:
        return "Wage Bill already Created"
    return "Wage Bill Created"


@shared_task
def send_wage_created_email_task():
    wage_bill = get_current_wage_bill()
    users = get_users()
    receiver_emails = []
    for user in users:
        receiver_emails.append(user.email)

    mail = WageBillCreatedMail(wage_bill=wage_bill, receivers=receiver_emails)
    mail.send_email()


@shared_task
def wage_sheets_submission_reminder():
    wage_bill = get_current_wage_bill()
    receiver_emails = []
    supervisors = get_supervisors()
    message = f"Please note that today is the last day for submitting wage sheets for wage bill week {wage_bill}." \
              f"If you have not submitted wage sheets, kindly do so."
    for user in supervisors:
        receiver_emails.append(user.email)
        Notification.objects.create(
            user=user,
            title="Wage Sheets Submission Reminder",
            message=message
        )
        if user.phone_number is not None:
            try:
                sms_notification = SMSNotification(
                    phone_number=user.phone_number,
                    first_name=user.first_name,
                    message=message
                )
                sms_notification.send()
            except TwilioRestException as e:
                print("Something went wrong with code :", e.code)
    mail = WageSheetsSubmissionReminder(wage_bill=wage_bill, receivers=receiver_emails)
    mail.send_email()


@shared_task
def wage_bill_created_notification():
    wage_bill = get_current_wage_bill()
    users = get_users()
    for user in users:
        Notification.objects.create(
            user=user,
            title="New Wage Bill Created",
            message=f"A new wage bill week {wage_bill} has been created. "
                    f"The deadline for processing wage sheets for the wage bill is {wage_bill.end_date}"
        )


@shared_task
def wage_bill_created_sms_notification():
    wage_bill = get_current_wage_bill()
    users = get_users()
    for user in users:
        if user.phone_number is not None:
            try:
                sms_notification = SMSNotification(
                    phone_number=user.phone_number,
                    first_name=user.first_name,
                    message=f"A new wage bill week {wage_bill} has been created. "
                            f"The deadline for processing wage sheets for the wage bill is {wage_bill.end_date}"
                )
                sms_notification.send()
            except TwilioRestException as e:
                print("Something went wrong with code :", e.code)

@shared_task
def wage_sheet_approver_notify(approver_user_id, wage_sheet_id):
    user = get_user_by_id(id=approver_user_id)
    wage_sheet: WageSheet = get_wage_sheet(id=wage_sheet_id)
    Notification.objects.create(
        user=user,
        title="New Wage Sheet Pending Approval",
        message=f"A new wage sheet from supervisor {wage_sheet.supervisor_user.name} and "
                f"field manager {wage_sheet.field_manager_user.name} is pending your approval"
    )
    mail = WageSheetApprovalNotification(wage_sheet=wage_sheet, receivers=[user.email])
    mail.send_email()
