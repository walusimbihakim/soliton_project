from projects.models.client_activity_pricing import ClientActivityRate
from .models import *

def get_all_clients():
    return Client.objects.all()

def get_client(client_id):
    return Client.objects.get(pk=client_id)

def get_client_contacts(client_id):
    return ClientContacts.objects.filter(pk=client_id)

def get_activity_client_rate(activity):
    try:
        rate = activity.clientactivityrate.rate
    except ClientActivityRate.DoesNotExist:
        rate = 0

    return rate