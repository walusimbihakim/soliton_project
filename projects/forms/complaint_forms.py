from django import forms
from crispy_forms.helper import FormHelper
from projects.models import Complaint



class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        exclude = ("wage_sheet",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()
