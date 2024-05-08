# forms.py 
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, label=_("Username"), widget=forms.TextInput(attrs={'placeholder': _('Username')}))
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={'placeholder': _('Email')}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'placeholder': _('Password')}))
    confirm_password = forms.CharField(label=_("Confirm Password"), widget=forms.PasswordInput(attrs={'placeholder': _('Confirm Password')}))
    first_name = forms.CharField(max_length=30, label=_("First Name"), widget=forms.TextInput(attrs={'placeholder': _('First Name')}))
    last_name = forms.CharField(max_length=30, label=_("Last Name"), widget=forms.TextInput(attrs={'placeholder': _('Last Name')}))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError(_("Passwords do not match."))
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(_("Username already exists. Please choose a different username."))
        return username

    def save(self):
        # Create the default User
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )

        # Create the associated CustomUser object
        custom_user = CustomUser.objects.create(
            user=user,
            bio='', 
            registration_method='normal',  
            email_verified=False,  
            two_factor_authentication=False,  
            # Add other fields as needed
        )
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': _('Username...')})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('Password...')})
    )