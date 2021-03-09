from crispy_forms.helper import FormHelper
from django import forms

from projects.models import FieldManager


class FieldManagerForm(forms.ModelForm):
    class Meta:
        model = FieldManager
        fields = "__all__"

        widgets = {
            "joining_date": forms.DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()
