from crispy_forms.helper import FormHelper
from django.forms import ModelForm, Textarea
from projects.models import UnitOfMeasure

class UnitOfMeasureForm(ModelForm):
    
    class Meta:
        model = UnitOfMeasure
        fields = ("unit_of_measure","description")

        widgets = {
            'description': Textarea()
        }

