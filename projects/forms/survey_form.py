from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab, Field

from projects.models.survey import *

class SurveyForm(forms.ModelForm):
    
    class Meta:
        model = Survey
        fields = (
            "project",
            "survey_date",
            "segmate",
            "survey_type", 
            "scope",
            "unit_of_measure", 
            "coordinates_lat", 
            "coordinates_long"
        )

    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)

       
