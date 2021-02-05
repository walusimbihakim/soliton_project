from django import forms
from crispy_forms.helper import FormHelper
from projects.models import WageSheet, Wage


class WageSheetForm(forms.ModelForm):
    class Meta:
        model = WageSheet
        fields = ("field_manager", "supervisor", "segment", "date", "description")

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()


class WageForm(forms.ModelForm):
    class Meta:
        model = Wage
        exclude = ("wage_sheet","is_manager_approved", "is_pm_approved", "is_gm_approved", "is_payed")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()
