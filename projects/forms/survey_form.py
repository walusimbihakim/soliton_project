from django.forms import ModelForm, HiddenInput, DateInput
from projects.models.survey import Survey
from projects.models.project_settings import UnitOfMeasure

units_of_measure = UnitOfMeasure.objects.all()


class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = (
            "project",
            "survey_date",
            "survey_type",
            "scope",
            "unit_of_measure",
            "coordinates_lat",
            "coordinates_long"
        )
        widgets = {
            'survey_date': DateInput(format='%m/%d/%Y', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.fields['project'].widget = HiddenInput()
