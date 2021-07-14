from decouple import config
from twilio.rest import Client

account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)
from_number: str = config('FROM_NUMBER')


class SMSNotification:
    def __init__(self, first_name, phone_number: str, message: str):
        self.phone_number: str = phone_number
        self.first_name = first_name
        self.message = message
        self.client = client

    def send(self) -> None:
        self.client.messages.create(
            body=f"Hello {self.first_name}, {self.message}\nFrom https://2jenge.com",
            from_=from_number,
            to=f"+256{self.phone_number}"
        )
