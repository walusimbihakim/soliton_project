from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse

from .selectors import *
from .forms import *

def clients_page_view(request):
    form = ClientForm(request.POST, request.FILES)
    
    if request.method=="POST":      
        if form.is_valid():
            form.save()

            redirect('manage_clients')
    
    clients = Client.objects.all()
    context ={
        'clients': clients, 
        'form': form,
    }
    return render(request, "manage_clients.html", context)

def add_client_contact(request):
    if request.method == "POST":
        contact_type = request.POST.get('contact_type')
        contacts = request.POST.get('contact')
        client = Client.objects.latest('id')

        contact = ClientContacts(
            contact_type=contact_type,
            contact=contacts, 
            client = client
            )
        
        contact.save()

        messages.success(request, f'Client Contact added Successfully')

        return JsonResponse({'success': True})

def delete_client(request):
    client_id = request.POST.get('id')

    client = get_client(client_id)

    client.delete()
    messages.success(request, f'Client {client} has been deleted Successfully')

    return  JsonResponse({'success': True})