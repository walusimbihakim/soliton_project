from django.db import models
from model_utils.models import TimeStampedModel
from clients.models import Client
from .projects import Project


class Site(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=50, null=True)
    is_deleted = models.BooleanField(default=False, null=True)
    is_completed = models.BooleanField(default=False, null=True)
    is_accessible = models.BooleanField(default=False, null=True)
    is_surveyed = models.BooleanField(default=False, null=True)
    is_accepted = models.BooleanField(default=False, null=True)
    site_location = models.CharField(null=True, blank=True, max_length=150)
    location_lat = models.CharField(max_length=20, null=True)
    location_long = models.CharField(max_length=20, null=True)
    start_date = models.DateField(null=True)
    survey_date = models.DateField(null=True)
    expected_end_date = models.DateField(null=True)
    current_stage = models.IntegerField(default=0)
    archivedStatus = models.BooleanField(default=False)
    ackStatus = models.BooleanField(default=False)
    ack_date = models.DateField(null=True)
    survey_time = models.CharField(max_length=255, null=True, blank=True)
    can_client_view_survey_reports = models.BooleanField(default=False)
    email_remainder_sent = models.BooleanField(default=False)
    site_contact_person = models.CharField(null=True, blank=True, max_length=150)
    site_contact_phone_number = models.IntegerField(null=True, blank=True)
    is_connected = models.BooleanField(default=False)
    is_ready_for_connection = models.BooleanField(default=False)
    is_connection_request_acknowledged = models.BooleanField(default=False)
    site_connection_date = models.DateTimeField(null=True, blank=True)
    number_of_fleet_on_site = models.IntegerField(null=True, blank=True)
    number_of_members_on_site = models.IntegerField(null=True, blank=True)
    site_image = models.FileField(upload_to="sites/", null=True, blank=True)
    isp_works_complete = models.BooleanField(default=False, null=True)
    osp_works_complete = models.BooleanField(default=False, null=True)
    ofc_works_complete = models.BooleanField(default=False, null=True)
    site_powering_complete = models.BooleanField(default=False, null=True)
    original_trenching_distance = models.IntegerField(null=True, blank=True)
    current_trenching_distance = models.IntegerField(null=True, blank=True)
    site_drawing = models.FileField(upload_to="drawing/", null=True, blank=True)
    site_address = models.TextField(null=True, blank=True)
    site_usd_rate = models.IntegerField(null=True, blank=True)
    site_type_choices = (
        ('single', 'Single'),
        ('dual', 'Dual'),
        ('shared', 'Shared'),
    )
    site_type = models.CharField(max_length=150, choices=site_type_choices, null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     clientId = self.clientId
    #     ackStatus = self.ackStatus
    #     print(ackStatus)
    #     note = 'Survey request was acknowledged'
    #     super(Site, self).save(*args, **kwargs)

        # if ackStatus == True:
        #     print(note)
        #     p = Notification(user=clientId, notification=note)
        #     p.save()

    def __str__(self):
        return self.id


class SiteImage(TimeStampedModel):
    status_choices = (
        ('before', 'before'),
        ('after', 'after'),
    )
    site = models.ForeignKey(to=Site, on_delete=models.CASCADE)
    image = models.FileField(upload_to="siteimages")
    lat = models.DecimalField(max_digits=12, decimal_places=12, null=True, blank=True)
    long = models.DecimalField(max_digits=12, decimal_places=12, null=True, blank=True)
    status = models.CharField(choices=status_choices, max_length=255)


class SiteDocument(TimeStampedModel):
    site = models.ForeignKey(to=Site, on_delete=models.CASCADE)
    file = models.FileField(upload_to="sitedocuments")
    title = models.CharField(max_length=255, null=True, blank=True)


class SitePIP(TimeStampedModel):
    site = models.ForeignKey(to=Site, on_delete=models.CASCADE)
    task = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()


class SitePower(TimeStampedModel):
    type_choices = (
        ('bts', 'BTS'),
        ('bts', 'Bts'),
        ('dual', 'DUAL'),
        ('dual', 'Dual'),
        ('single', 'SINGLE'),
        ('single', 'Single')
    )
    site = models.ForeignKey(to=Site, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    # user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    material_used = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    powering_successful = models.BooleanField(null=True, blank=True)
    product = models.CharField(max_length=255, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    equipment_used = models.CharField(max_length=255, null=True, blank=True)

class Siteboq(TimeStampedModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True, related_name="siteboq_site")
    material = models.CharField(max_length=50, null=True, blank=True)
    actual_quantity = models.IntegerField(null=True, blank=True)
    estimate_quantity = models.IntegerField(null=True, blank=True)
    boq_type = models.CharField(max_length=50, null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="siteboq_user")
    description = models.CharField(max_length=255, null=True, blank=True)

