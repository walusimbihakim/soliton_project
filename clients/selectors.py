from .models import *

def get_all_clients():
    return Client.objects.all()

def get_client(client_id):
    return Client.objects.get(pk=client_id)

def get_client_contacts(client_id):
    return ClientContacts.objects.filter(pk=client_id)