from django import forms
from django.contrib.auth import get_user_model
from django.forms.widgets import HiddenInput
from crispy_forms.helper import FormHelper

from projects.constants import FIELD_MANAGER
from projects.models import WageSheet, Wage


class WageSheetForm(forms.ModelForm):
    class Meta:
        model = WageSheet
        fields = ("wage_bill", "date", "description", "segment", "field_manager_user")
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()
        self.fields["wage_bill"].widget = HiddenInput()

        # field_manager_users = get_user_model().objects.filter(user_role=FIELD_MANAGER)
        # field_manager_users = [(int(field_manager_user.id), field_manager_user.name)
        #                        for field_manager_user in field_manager_users]
        # self.fields['field_manager_user'] = forms.ChoiceField(choices=field_manager_users)


class WageForm(forms.ModelForm):
    class Meta:
        model = Wage
        exclude = ("wage_sheet", "is_manager_approved", "is_pm_approved", "is_gm_approved", "is_payed")

    def __init__(self, *args, **kwargs):
        super(WageForm, self).__init__(*args, **kwargs)
        self.fields['payment'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
