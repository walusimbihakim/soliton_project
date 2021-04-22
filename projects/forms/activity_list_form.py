from django import forms
from crispy_forms.helper import FormHelper
from projects.models.activity_list import Activity


class ActivityListForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            "code",
            "name",
            "unit_cost",
            "unit_of_measure",
            "is_fd_underground",
            "is_fd_arial",
            "is_site_connection",
            "is_tower_construction",
            "is_lan_installation",
            "is_equipment_installation",
            "is_manhole_installation",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
