from django import forms
from crispy_forms.helper import FormHelper
from projects.models import Worker


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = "__all__"

        widgets = {
            "joining_date": forms.DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()
