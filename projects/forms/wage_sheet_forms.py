from django import forms
from crispy_forms.helper import FormHelper
from projects.models import WageSheet, Wage


class WageSheetForm(forms.ModelForm):
    class Meta:
        model = WageSheet
        fields = "__all__"

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()


class WageForm(forms.ModelForm):
    class Meta:
        model = Wage
        exclude = ("wage_sheet",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()
