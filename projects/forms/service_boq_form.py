from django import forms
from crispy_forms.helper import FormHelper

from projects.models.boqs import MaterialBOQItem, ServiceBOQItem


class ServiceBOQForm(forms.ModelForm):
    class Meta:
        model = ServiceBOQItem
        fields = ("activity", "quantity","description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()
