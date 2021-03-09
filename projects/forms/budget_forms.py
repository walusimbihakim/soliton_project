from crispy_forms.helper import FormHelper
from django.forms import ModelForm, Textarea, HiddenInput

from projects.models.budget import MaterialBudget, ExecutionBudget, ExpenseBudget

class MaterialBudgetForm(ModelForm):
    
    class Meta:
        model = MaterialBudget
        fields = ("budget", "material", "quantity", "unit_cost", "total_cost")

    def __init__(self, *args, **kwargs):
        super(MaterialBudgetForm, self).__init__(*args, **kwargs)

        self.fields['budget'].widget = HiddenInput()
        self.fields['total_cost'].widget.attrs['readonly'] = True
        self.fields['unit_cost'].widget.attrs['readonly'] = True

        self.helper = FormHelper()

class ExecutionBudgetForm(ModelForm):
    
    class Meta:
        model = ExecutionBudget
        fields = ("budget", "quantity", "unit_cost", "total_cost")

    def __init__(self, *args, **kwargs):
        super(ExecutionBudgetForm, self).__init__(*args, **kwargs)

        self.fields['budget'].widget = HiddenInput()
        self.fields['total_cost'].widget.attrs['readonly'] = True
        self.fields['unit_cost'].widget.attrs['readonly'] = True

        self.helper = FormHelper()

class ExpenseBudgetForm(ModelForm):
    
    class Meta:
        model = ExpenseBudget
        fields = ("budget", "expense", "quantity", "rate", "total_cost")

    def __init__(self, *args, **kwargs):
        super(ExpenseBudgetForm, self).__init__(*args, **kwargs)

        self.fields['budget'].widget = HiddenInput()
        self.fields['total_cost'].widget.attrs['readonly'] = True
        self.fields['rate'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
