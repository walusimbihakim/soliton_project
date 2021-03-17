from django.contrib import admin

# Register your models here.
from projects.models import Worker, Survey, ExecutionScope, Team, FieldManager, \
    PIPTeam, WageSheet, Wage, Activity, Project
from projects.models.boqs import BOQ, MaterialBOQItem, ServiceBOQItem
from projects.models.client_activity_rates import ClientActivityRate
from projects.models.materials import Material
from projects.models.segments import Segment
from projects.models.users import User

admin.site.register(Project)
admin.site.register(Worker)
admin.site.register(Survey)
admin.site.register(BOQ)
admin.site.register(MaterialBOQItem)
admin.site.register(Material)
admin.site.register(ServiceBOQItem)
admin.site.register(ClientActivityRate)
admin.site.register(ExecutionScope)
admin.site.register(Team)
admin.site.register(FieldManager)
admin.site.register(PIPTeam)
admin.site.register(WageSheet)
admin.site.register(Wage)
admin.site.register(Segment)
admin.site.register(Activity)
admin.site.register(User)

