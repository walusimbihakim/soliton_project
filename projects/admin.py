from django.contrib import admin

# Register your models here.
from projects.models import Worker, Survey
from projects.models.boqs import BOQ

admin.site.register(Worker)
admin.site.register(Survey)
admin.site.register(BOQ)