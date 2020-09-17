from projects.models.boqs import BOQ, MaterialBOQItem, ServiceBOQItem


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
