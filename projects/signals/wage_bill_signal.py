from django.db.models.signals import post_save
from django.dispatch import receiver
from projects.models import WageBill
from projects.tasks import send_wage_created_email_task


@receiver(post_save, sender=WageBill)
def new_wage_bill_added(sender, **kwargs):
    if kwargs["created"]:
        send_wage_created_email_task.delay()
