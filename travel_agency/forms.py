from django.contrib.auth.models import User
from django import forms
from .models import Search


class DateInput(forms.DateInput):
    input_type = 'date'

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ['from_location', 'to_location', 'from_date', 'to_date', 'travelers_count']
        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput(),
        }
        initial = {
            'travelers_count': 1
        }