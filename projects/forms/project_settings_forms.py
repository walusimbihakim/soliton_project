from crispy_forms.helper import FormHelper
from django.forms import ModelForm, Textarea
from projects.models import UnitOfMeasure
from projects.models.budget import Expense

class UnitOfMeasureForm(ModelForm):
    
    class Meta:
        model = UnitOfMeasure
        fields = ("unit_of_measure","description")

        widgets = {
            'description': Textarea()
        }

class ExpenseForm(ModelForm):
    
    class Meta:
        model = Expense
        fields = ('expense', "description")

