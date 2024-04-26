from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product


class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

class UserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        (1, 'Customer'),
        (2, 'Seller'),
    )
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'remaining'] 