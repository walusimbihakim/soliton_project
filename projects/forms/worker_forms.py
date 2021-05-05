from django import forms
from crispy_forms.helper import FormHelper
from projects.models import Worker, GroupWorker


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        exclude = ('registered_by_user',)

        widgets = {
            "joining_date": forms.DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()


class GroupWorkerForm(forms.ModelForm):
    class Meta:
        model = GroupWorker
        exclude = ('supervisor',)

    def __init__(self, user=None, *args, **kwargs):
        super(GroupWorkerForm, self).__init__(*args, **kwargs)
        self.fields['workers'].queryset = Worker.objects.filter(registered_by_user=user)
        self.helper = FormHelper()


