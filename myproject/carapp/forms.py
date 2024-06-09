from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Phone Number', max_length=9)

class SearchForm(forms.Form):
    license_plate = forms.CharField(
        max_length=20,
        label='',  # Esto oculta el label
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter license plate'
        })
    )