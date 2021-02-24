from django import template

from projects.models.materials import Material
from projects.models.activity_list import Activity
from projects.models.survey import Survey

from clients.selectors import get_client_activity_rate


register = template.Library()

@register.filter
def material_name_filter(material_id):
    return Material.objects.get(pk=material_id)

@register.filter
def material_unitcost_filter(material_id):
    material = Material.objects.get(pk=material_id)

    return "{:,}".format(material.unit_cost)

@register.filter
def material_totalcost_filter(material_id, quantity):
    material = Material.objects.get(pk=material_id)

    total_cost = (quantity*material.unit_cost)

    return "{:,}".format(total_cost)

@register.filter
def activity_name_filter(activity_id):
    return Activity.objects.get(pk=activity_id)

@register.filter
def activity_unitcost_filter(activity_id, client_id):
    try:
        client_rate = get_client_activity_rate(client_id, activity_id)

        rate = client_rate.rate
    except:
        rate = 0

    return rate

@register.filter
def activity_totalcost_filter(quantity, rate):
    total_cost = (quantity*rate)

    return "{:,}".format(total_cost)

@register.filter
def survey_filter(survey_id):
    return Survey.objects.get(pk=survey_id)

