from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab, Field
from projects.models.projects import Project, ProjectWorks, DuctSystem, ProjectType

class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = (
            "project_code", 
            "name", 
            "client", 
            "description", 
            "start_date",
            "expected_end_date"
            )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Basic Information',
                    Field('project_code', css_class="col-md-3"),
                    Field('name', wrapper_class="col-md-9"),
                    Field('client', wrapper_class="col-md-3"),
                    Field('description', wrapper_class="col-md-9"),
                    Field('start_date', wrapper_class="col-md-6"),
                    Field('expected_end_date', wrapper_class="col-md-6"),
                ),
                Tab(
                    ('Settings'),
                )
            )
        )

class ProjectTypeForm(forms.ModelForm):
    
    class Meta:
        model = ProjectType
        fields = ("code", "project_type", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.Helper = FormHelper()

class DuctForm(forms.ModelForm):
    
    class Meta:
        model = DuctSystem
        fields = ("duct_code", "duct_type", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.Helper = FormHelper()
