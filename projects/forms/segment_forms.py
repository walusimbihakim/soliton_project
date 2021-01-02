from django import forms
from crispy_forms.helper import FormHelper
from projects.models import Segment


class SegmentForm(forms.ModelForm):
    class Meta:
        model = Segment
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Helper = FormHelper()
