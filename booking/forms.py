from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BusSearchForm(forms.Form):
    from_city = forms.CharField(max_length=100)
    to_city = forms.CharField(max_length=100)
    journey_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    

class BookingForm(forms.Form):
    # name = forms.CharField(max_length=100)
    # email = forms.EmailField()
    
    
    # name = forms.CharField(
    #     label="Your Name",
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'style': 'border: 2px solid #007bff; padding: 10px; border-radius: 5px;',# Bootstrap class
    #         'placeholder': 'Enter your name',
    #     })
    # )
    # email = forms.EmailField(
    #     label="Email Address",
    #     widget=forms.EmailInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Enter your email',
    #         'style': 'border: 2px solid #28a745; padding: 10px; border-radius: 5px;',
    #     })
    # )
    name = forms.CharField(
        label="Your Name",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors duration-200',
            'placeholder': 'Enter your name',
            'required': True,
        }),
        error_messages={
            'required': 'Please enter your name'
        }
    )
    
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors duration-200',
            'placeholder': 'Enter your email',
            'required': True,
        }),
        error_messages={
            'required': 'Please enter your email',
            'invalid': 'Please enter a valid email address'
        }
    )
    
    #seat_number = forms.IntegerField()
    
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    

