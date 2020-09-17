from django.contrib import admin

# Register your models here.
from projects.models import Worker, Survey
from projects.models.boqs import BOQ, MaterialBOQItem, ServiceBOQItem
from projects.models.client_activity_rates import ClientActivityRate
from projects.models.materials import Material

admin.site.register(Worker)
admin.site.register(Survey)
admin.site.register(BOQ)
admin.site.register(MaterialBOQItem)
admin.site.register(Material)
admin.site.register(ServiceBOQItem)
admin.site.register(ClientActivityRate)