from django import forms
from django.forms.widgets import HiddenInput
from crispy_forms.helper import FormHelper

from projects.constants import FIELD_MANAGER
from projects.models import WageSheet, Wage, Worker, User, Activity, GroupWorker
from projects.models.wage_sheets import GroupWage
from projects.selectors.wage_bill_selectors import get_current_wage_bill


class WageSheetForm(forms.ModelForm):
    class Meta:
        model = WageSheet
        fields = ("wage_bill", "date", "description", "segment", "field_manager_user")
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "description": forms.TextInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['field_manager_user'].queryset = User.objects.filter(user_role=FIELD_MANAGER)
        self.Helper = FormHelper()
        self.fields["wage_bill"].widget = HiddenInput()


class WageForm(forms.ModelForm):
    class Meta:
        model = Wage
        fields = ["worker", "activity", "quantity", "payment"]

    def __init__(self, user=None, *args, **kwargs):
        super(WageForm, self).__init__(*args, **kwargs)
        self.fields['worker'].queryset = Worker.objects.filter(assigned_to=user)
        self.fields['activity'].queryset = Activity.objects.filter(type=user.type, is_group=False)
        self.fields['payment'].widget.attrs['readonly'] = True
        self.helper = FormHelper()


class GroupWageForm(forms.ModelForm):
    class Meta:
        model = GroupWage
        exclude = ("wage_sheet",)

    def __init__(self, user=None, *args, **kwargs):
        super(GroupWageForm, self).__init__(*args, **kwargs)
        self.fields['group_worker'].queryset = GroupWorker.objects.filter(supervisor=user)
        self.fields['activity'].queryset = Activity.objects.filter(type=user.type, is_group=True)
        self.fields['payment'].widget.attrs['readonly'] = True
        self.helper = FormHelper()


class WageFromPhoneNumberForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=10, required=False)

    class Meta:
        model = Wage
        fields = ["phone_number", "activity", "quantity", "payment"]

    def __init__(self, user=None, *args, **kwargs):
        super(WageFromPhoneNumberForm, self).__init__(*args, **kwargs)
        self.fields['activity'].queryset = Activity.objects.filter(type=user.type, is_group=False)
        self.fields['payment'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
