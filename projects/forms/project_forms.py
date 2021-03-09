from django.forms import ModelForm, DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab, Field
from projects.models.projects import Project, ProjectWorks, DuctSystem, ProjectType


class ProjectForm(ModelForm):
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
        widgets = {
            'start_date': DateInput(format=('%m/%d%/Y'), attrs={'type': 'date'}),
            'expected_end_date': DateInput(format=('%m/%d/%Y'), attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

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
        self.helper.form_show_errors = False


class ProjectTypeForm(ModelForm):
    class Meta:
        model = ProjectType
        fields = ("code", "project_type", "description")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Helper = FormHelper()


class DuctForm(ModelForm):
    class Meta:
        model = DuctSystem
        fields = ("duct_code", "duct_type", "description")

    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)

        self.Helper = FormHelper()
        self.Helper.form_show_errors = False


