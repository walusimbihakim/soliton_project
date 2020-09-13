from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab, Field

from projects.models import Worker
from projects.models.projects import Project, ProjectWorks, DuctSystem, ProjectType


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()


