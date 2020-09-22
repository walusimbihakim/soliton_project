from django.forms import ModelForm, HiddenInput, DateInput, ChoiceField, Select
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab, Field

from projects.models.survey import Survey
from projects.models.project_settings import UnitOfMeasure

units_of_measure = UnitOfMeasure.objects.all()

class SurveyForm(ModelForm):
    # forms.ChoiceField(, choices=[CHOICES], required=False) FormsTools.EmployeesToTuples(
    
    # units_of_measure = UnitOfMeasure.objects.all()

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
        widgets = {
            'survey_date': DateInput(format=('%m/%d/%Y'), attrs={'type': 'date'}),
            # 'unit_of_measure': ChoiceField(choices=list(units_of_measure))
        }

    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)

        self.fields['project'].widget = HiddenInput()

       
