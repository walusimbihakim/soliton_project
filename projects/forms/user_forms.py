from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from projects.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number","email",
                  "username", "user_role", "type", "is_active", "is_staff",
                  "is_superuser")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
