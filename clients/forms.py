from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab, Field
from .models import *


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
