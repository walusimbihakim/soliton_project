from django import forms
from projects.models import ExecutionScope


class ExecutionScopeForm(forms.ModelForm):
    class Meta:
        model = ExecutionScope
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
