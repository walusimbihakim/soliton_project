from abc import ABCMeta, abstractmethod
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from projects.models import WageBill


class Mail(metaclass=ABCMeta):
    def __init__(self):
        self.receivers: list = []
        self.context: dict = {}
        self.__subject: str = ""
        self.__template_uri: str = ""
        self.__from_email = None
        self.create_mail()

    @abstractmethod
    def create_mail(self):
        pass

    def set_subject(self, subject):
        self.__subject = subject

    def set_template_uri(self, template_uri):
        self.__template_uri = template_uri

    def get_template_uri(self):
        return self.__template_uri

    def set_receivers(self, receivers):
        self.receivers = receivers

    def get_receivers(self):
        return self.receivers

    def send_email(self):
        html_content = get_template(self.__template_uri).render(self.context)
        msg = EmailMultiAlternatives(self.__subject, None, None, self.receivers)
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class WageBillCreatedMail(Mail):
    def __init__(self, wage_bill, receivers):
        super().__init__()
        self.receivers: list = receivers
        self.context = {
            "wage_bill": wage_bill
        }

    def create_mail(self):
        self.set_subject("New Wage Bill Added")
        self.set_template_uri("email/wage_bill_created_email.html")
