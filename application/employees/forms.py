
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['photo', 'full_name', 'email', 'mobile', 'date_of_birth']
        widgets={
            'date_of_birth':forms.DateInput(attrs={'type': 'date','class':'datepicker'})
        }
