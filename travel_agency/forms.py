from django.contrib.auth.models import User
from django import forms
from .models import *
from django.utils.translation import gettext as _


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
    round_trip = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    price_choices = (
        (0, _("None")),
        (1, _("$->$$$")),
        (2, _("$$$->$"))
    )
    price = forms.ChoiceField(choices=price_choices, required=False)
    time_choices = (
        (0, _("None")),
        (1, _("Shortest->Longest")),
        (2, _("Longest->Shortest"))
    )
    time = forms.ChoiceField(choices=time_choices, required=False)
    review_choices = (
        (0, _("None")),
        (1, _("Lowest Ratings")),
        (2, _("Highest Ratings"))
    )
    review = forms.ChoiceField(choices=review_choices, required=False)
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

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'home_addr', 'billing_addr', 'payment_method', 'email']
