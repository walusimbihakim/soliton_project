from django import forms
from crispy_forms.helper import FormHelper
from projects.models import Complaint, Worker, Activity


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        exclude = ("wage_sheet", "is_manager_approved", "is_pm_approved", "is_gm_approved", "is_payed", "remarks")
        widgets = {
            "description": forms.TextInput()
        }

    def __init__(self, user=None, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args, **kwargs)
        self.fields['worker'].queryset = Worker.objects.filter(registered_by_user=user)
        self.fields['activity'].queryset = Activity.objects.filter(type=user.type)
        self.helper = FormHelper()
