from io import BytesIO

from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.db.models import Sum


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def is_date_between(date, start_date, end_date):
    return start_date <= date <= end_date


def calculate_airtel_charge(amount):
    if amount <= 2500:
        charge = 330
    elif amount <= 5000:
        charge = 440
    elif amount <= 15000:
        charge = 700
    elif amount <= 30000:
        charge = 880
    elif amount <= 45000:
        charge = 1210
    elif amount <= 60000:
        charge = 1500
    elif amount <= 125000:
        charge = 1925
    elif amount <= 250000:
        charge = 3575
    elif amount <= 500000:
        charge = 7000
    else:
        charge = 12500
    return charge


def calculate_total_wages(wages) -> int:
    if not wages:
        return 0
    sum = wages.aggregate(Sum('payment'))
    payment = sum['payment__sum']
    return payment


def calculate_total_consolidated_payments(consolidated_payments) -> int:
    if not consolidated_payments:
        return 0
    sum = consolidated_payments.aggregate(Sum('total_payment'))
    payment = sum['total_payment__sum']
    return payment
