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
    from_location = forms.CharField(widget=forms.TextInput())
    to_location = forms.CharField(widget=forms.TextInput())
    travelers_count = forms.IntegerField(widget=forms.NumberInput())

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('travelers_count') < 1:
            raise forms.ValidationError(u'Please enter at least 1 traveler.')

    class Meta:
        model = Search
        fields = ['from_date', 'to_date']
        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput()
        }