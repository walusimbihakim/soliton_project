from django.forms import ModelForm, DateInput
from crispy_forms.helper import FormHelper

from projects.models.wage_bills import WageBill

class WageBillForm(ModelForm):
    
    class Meta:
        model = WageBill
        fields = ("start_date", "end_date")

        widgets = {
            "start_date": DateInput(attrs={"type": "date"}),
            "end_date": DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super(WageBillForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

