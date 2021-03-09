from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab, Field
from projects.models.sites import * 

class SiteForm(forms.ModelForm):
    
    class Meta:
        model = Site
        fields = ("site_name", "site_location", "site_image", "project", "site_type")
