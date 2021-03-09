from django import forms
from crispy_forms.helper import FormHelper
from projects.models import Team, PIPTeam


class PIPTeamForm(forms.ModelForm):
    class Meta:
        model = PIPTeam
        exclude = ('date',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()
