from django.contrib import admin

# Register your models here.
from projects.models import Worker, Survey, ExecutionScope, Team, FieldManager, \
    PIPTeam, WageSheet, Wage, Activity, Project, WageBill, GroupWorker, Complaint, Notification, Deduction
from projects.models.boqs import BOQ, MaterialBOQItem, ServiceBOQItem
from projects.models.client_activity_rates import ClientActivityRate
from projects.models.materials import Material
from projects.models.segments import Segment
from projects.models.users import User
from projects.models.wage_bills import ConsolidatedWageBillPayment
from projects.models.wage_sheets import GroupWage
from projects.models.workers import WorkerAssignment

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
admin.site.register(WageBill)
admin.site.register(GroupWorker)
admin.site.register(WorkerAssignment)
admin.site.register(Complaint)
admin.site.register(GroupWage)
admin.site.register(ConsolidatedWageBillPayment)
admin.site.register(Notification)
admin.site.register(Deduction)
