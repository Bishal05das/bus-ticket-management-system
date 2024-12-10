from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BusSearchForm(forms.Form):
    from_city = forms.CharField(max_length=100)
    to_city = forms.CharField(max_length=100)
    journey_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    

class BookingForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    #seat_number = forms.IntegerField()
    
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    

