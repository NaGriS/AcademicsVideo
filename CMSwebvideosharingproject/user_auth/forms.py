
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    #password=forms.CharField(widget=forms.PasswordInput)
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=("Enter the same password as above, for verification."))

    class Meta:
        model= User
        fields=['username','first_name','last_name','email','password1']

    #error two passwords not match
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2





