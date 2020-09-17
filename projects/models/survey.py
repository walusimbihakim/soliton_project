from django.db import models
from model_utils.models import TimeStampedModel

from projects.models.sites import Site
from projects.models.projects import Project


class Survey(TimeStampedModel):
    survey_type_choices = (
        ('FD-UG', 'Fibre Underground'),
        ('FD-Aerial', 'Fibre Aerial'),
        ('Site', 'Site'),
        ('LAN', 'LAN'),
        ('Tower', 'Tower'),
        ('Equipment', 'Equipment'),
    )
    survey_date = models.DateField(auto_now=False, auto_now_add=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    survey_type = models.CharField(max_length=50, choices=survey_type_choices)
    scope = models.IntegerField()
    unit_of_measure = models.CharField(max_length=15)
    coordinates_lat = models.CharField(max_length=20, null=True)
    coordinates_long = models.CharField(max_length=20, null=True)
    surveyor = models.CharField(max_length=50, null=True, blank=True)
    is_checked = models.BooleanField(default=False)
    checked_by = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=50)
    client_approved = models.BooleanField(default=False)

    def __str__(self):
        return "Survey {} at {},{}".format(self.id, self.coordinates_lat, self.coordinates_long)


class SurveyResult(TimeStampedModel):
    file_url = models.FileField(upload_to='files', null=True)
    title = models.CharField(max_length=50, null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True, related_name="surveyresult_site")
    surveyor = models.CharField(max_length=50, null=True, blank=True)
    acceptStatus = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        surveyor = self.surveyor
        acceptStatus = self.acceptStatus
        note1 = 'Pending Review'
        note2 = 'survey_results_accepted'
        note3 = 'Survey results were rejected'

        if acceptStatus == None:
            print("Pending Review")
            p = Notification(user=surveyor, notification=note1)
            p.save()
            super(SurveyResult, self).save(*args, **kwargs)

        elif acceptStatus == True:  # shouldn't do this
            print("survey_results_accepted")
            p = Notification(user=surveyor, notification=note2)
            p.save()
            super(SurveyResult, self).save(*args, **kwargs)

        else:
            print("Survey results were rejected")
            p = Notification(user=surveyor, notification=note3)
            p.save()
            super(SurveyResult, self).save(*args, **kwargs)


class SurveyResultComment(TimeStampedModel):
    survey_result = models.ForeignKey(SurveyResult, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="SurveyResult_survey_result")
    comment = models.CharField(max_length=255)
    readStatus = models.BooleanField(default=False)
    surveyor = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        surveyor = self.surveyor
        note = 'There is a new comment on the uploaded survey resutls'
        print("There is a new comment on the uploaded survey resutls")
        p = Notification(user=surveyor, notification=note)
        p.save()
        super(SurveyResultComment, self).save(*args, **kwargs)
