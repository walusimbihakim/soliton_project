from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


class Mail(object):
    FROM_EMAIL = None

    def __init__(self, subject, template_uri, receivers, context=None):
        self.__receivers: list = receivers
        self.__context: dict = context
        self.__subject: str = subject
        self.__template_uri: str = template_uri

    def send_email(self):
        html_content = get_template(self.__template_uri).render(self.__context)
        msg = EmailMultiAlternatives(self.__subject, None, self.FROM_EMAIL, self.__receivers)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
