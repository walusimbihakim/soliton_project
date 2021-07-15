from celery.app import shared_task
from projects.classes.mails import WageSheetsSubmissionReminder
from projects.selectors.user_selectors import get_supervisors
from projects.selectors.wage_bill_selectors import get_current_wage_bill
from projects.services.notification_services import create_notification
from projects.tasks.random import create_sms_notification

WAGE_SHEET_SUBMISSION_REMINDER_MESSAGE = f"Please note that today is the last day for submitting wage sheets for wage " \
                                         f"bill week {get_current_wage_bill()}." \
                                         f"If you have not submitted wage sheets, kindly do so."


@shared_task
def wage_sheets_submission_reminder():
    wage_bill = get_current_wage_bill()
    receiver_emails = []
    supervisors = get_supervisors()
    message = WAGE_SHEET_SUBMISSION_REMINDER_MESSAGE
    for user in supervisors:
        receiver_emails.append(user.email)
        create_notification(
            user,
            "Wage Sheets Submission Reminder",
            message
        )
        create_sms_notification.delay(user.id, message)
    mail = WageSheetsSubmissionReminder(wage_bill=wage_bill, receivers=receiver_emails)
    mail.send_email()
