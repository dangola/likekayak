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
    to_location = forms.CharField(widget=forms.TextInput(), required=False)
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
    non_stop = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    one_stop = forms.BooleanField(widget=forms.CheckboxInput, required=False)
    
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

class CarSearchForm(forms.Form):
    from_date =  forms.DateField(widget=DateInput())
    to_date =  forms.DateField(widget=DateInput())
    pickup_location = forms.CharField(widget=forms.TextInput())
    dropoff_location = forms.CharField(widget=forms.TextInput())
    same_drop_off = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    price_choices = (
        (0, _("None")),
        (1, _("$->$$$")),
        (2, _("$$$->$"))
    )
    price = forms.ChoiceField(choices=price_choices, required=False)
   
class HotelsForm(forms.ModelForm):
    location = forms.CharField(widget=forms.TextInput())
    rooms_count = forms.IntegerField(widget=forms.NumberInput())
    breakfast = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    parking = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    pool = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    gym = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    bar = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    wifi = forms.BooleanField(widget=forms.CheckboxInput(), required=False)


    class Meta:
        model = Hotel
        fields = ['from_date', 'to_date']
        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput()
        }

class ReviewForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    rating = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'star'}), choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),))

    class Meta:
        model = Review
        fields = ['content']
        widgets = {
          'content': forms.Textarea(attrs={'rows':10, 'cols':70}),
        }

class CruiseSearchForm(forms.ModelForm):
    from_location = forms.CharField(widget=forms.TextInput())
    to_location = forms.CharField(widget=forms.TextInput(), required=False)
    travelers_count = forms.IntegerField(widget=forms.NumberInput())
    class Meta:
        model = Cruise
        fields = ['from_date', 'to_date']
        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput()
        }

