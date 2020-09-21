from crispy_forms.helper import FormHelper
from django import forms
from projects.models import ExecutionScope


class ExecutionScopeForm(forms.ModelForm):
    class Meta:
        model = ExecutionScope
        fields = ("quantity", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()
