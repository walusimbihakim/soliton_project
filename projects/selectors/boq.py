from projects.models.boqs import BOQ, MaterialBOQItem, ServiceBOQItem
from django.db.models import Sum


def get_boq(id):
    return BOQ.objects.get(pk=id)


def get_materialboqitems(boq):
    return MaterialBOQItem.objects.filter(boq=boq)


def get_serviceboqitems(boq):
    return ServiceBOQItem.objects.filter(boq=boq)


def get_material_boq_item(id: int) -> MaterialBOQItem:
    material_boq_item = MaterialBOQItem.objects.get(pk=id)
    return material_boq_item


def get_service_boq_item(id: int) -> ServiceBOQItem:
    service_boq_item = ServiceBOQItem.objects.get(pk=id)
    return service_boq_item

def get_project_material_boqs(surveys):
    boqs = BOQ.objects.filter(survey__in=surveys)
    material_boqs = MaterialBOQItem.objects.filter(boq__in = boqs)
    material_boqs_totals = material_boqs.values('material').annotate(material_total=Sum('quantity'))

    return material_boqs_totals

def get_project_service_boqs(surveys):
    boqs = BOQ.objects.filter(survey__in=surveys)
    service_boqs = ServiceBOQItem.objects.filter(boq__in = boqs)
    service_boqs_totals = service_boqs.values('activity').annotate(activity_total=Sum('quantity'))

    return service_boqs_totals