from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'email', 'password']

class SearchForm(forms.ModelForm):
	class Meta:
		fields = ['from_location', 'to_location', 'from_date', 'to_date', 'travelers_count']
