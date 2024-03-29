from projects.models import User
from projects.models.notification import Notification


def create_notification(user: User, title: str, message: str) -> Notification:
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message
    )
    return notification




def read_all_notifications(notifications):
    for notification in notifications:
        notification.is_read = True
        notification.save()
