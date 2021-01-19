from django.forms import ModelForm, HiddenInput, DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab, Field

from projects.models.pip import PIP

class PIPForm(ModelForm):
    
    class Meta:
        model = PIP
        fields = ('scope', 'activity', 'start_date', 'end_date', 'dependencies')

        widgets = {
            'start_date': DateInput(format=('%m/%d/%Y'), attrs={'type':'date'}),
            'end_date': DateInput(format=('%m/%d/%Y'), attrs={'type':'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(PIPForm, self).__init__(*args, **kwargs)

        self.fields['scope'].widget = HiddenInput()

        self.helper = FormHelper()
        
