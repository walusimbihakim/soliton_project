from django import forms
from crispy_forms.helper import FormHelper

from projects.models.boqs import MaterialBOQItem


class MaterialBOQForm(forms.ModelForm):
    class Meta:
        model = MaterialBOQItem
        fields = ("material", "quantity")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()
