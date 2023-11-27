from django import forms
from django.db import models
from django.contrib.auth.models import User
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-label mb-5"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-label mb-5"}))


class UserRegistartionForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    #identity = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        help_texts = {
            'username': '',
            # 'other_field': 'Custom help text for another field if you want to keep/add',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']

class BuyCryptoForm(forms.Form):
    cryptocurrency = forms.ModelChoiceField(queryset=Cryptocurrency.objects.all(), empty_label=None, label='Cryptocurrency')
    quantity = forms.DecimalField(max_digits=15, decimal_places=6, label='Quantity')

class SellCryptoForm(forms.Form):
    quantity = forms.DecimalField(max_digits=15, decimal_places=6, label='quantity')

    def __init__(self, *args, user=None, **kwargs):
        super(SellCryptoForm, self).__init__(*args, **kwargs)
        # If user is provided, filter the cryptocurrency choices based on user holdings
        if user:
            user_holdings, created = UserCryptoHoldings.objects.get_or_create(user=user)
            allowed_cryptocurrencies = [
                (crypto.name, crypto.name)
                for crypto in Cryptocurrency.objects.filter(name__in=user_holdings.holdings.keys())
            ]

            self.fields['cryptocurrency'] = forms.ChoiceField(choices=allowed_cryptocurrencies, label='Cryptocurrency')
