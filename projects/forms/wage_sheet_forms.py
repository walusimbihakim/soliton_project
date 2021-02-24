from django import forms
from django.forms.widgets import HiddenInput
from crispy_forms.helper import FormHelper
from projects.models import WageSheet, Wage


class WageSheetForm(forms.ModelForm):
    class Meta:
        model = WageSheet
        fields = ("wage_bill", "field_manager", "supervisor", "segment", "date", "description")

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()

        self.fields["wage_bill"].widget = HiddenInput()


class WageForm(forms.ModelForm):
    class Meta:
        model = Wage
        exclude = ("wage_sheet","is_manager_approved", "is_pm_approved", "is_gm_approved", "is_payed")

    def __init__(self, *args, **kwargs):
        super(WageForm, self).__init__(*args, **kwargs)
        self.fields['payment'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
