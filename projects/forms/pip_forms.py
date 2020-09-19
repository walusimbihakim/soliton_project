from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab, Field

from projects.models.pip import PIP

class PIPForm(forms.ModelForm):
    
    class Meta:
        model = PIP
        fields = ('scope', 'activity', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        super(PIPForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
