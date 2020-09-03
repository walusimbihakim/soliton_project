from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab, Field
from .models import *

class ClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        fields = ("company_name", "adress", "email", "contact", "website","contact_person", "profile_pic")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Basic Information',
                    Field('company_name', css_class="col-md-12"),
                    Field('adress', wrapper_class="col-md-12"),
                    Field('email', wrapper_class="col-md-6"),
                    Field('contact', wrapper_class="col-md-6"),
                    Field('website', wrapper_class="col-md-6"),
                    Field('contact_person', wrapper_class="col-md-6"),
                    Field('profile_pic', wrapper_class="col-md-12"),
                ),
                Tab(
                    ('Settings'),
                )
            )
        )
