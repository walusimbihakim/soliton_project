from crispy_forms.helper import FormHelper
from django.forms import ModelForm, Textarea
from projects.models import ExecutionScope


class ExecutionScopeForm(ModelForm):

    class Meta:
        model = ExecutionScope
        fields = ("quantity", "description")
        widgets = {
            'description': Textarea()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['description'].widget = forms.Textarea
        self.Helper = FormHelper()
