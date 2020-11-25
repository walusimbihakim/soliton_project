from django import forms
from crispy_forms.helper import FormHelper
from projects.models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = "__all__"

        widgets = {
            "joining_date": forms.DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()
