
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    #password=forms.CharField(widget=forms.PasswordInput)
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        'email_none': ("please enter your email"),
        'first_name_none': ("please enter your first name"),
        'last_name_none': ("please enter your last name")
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

    #error fields email, first name, last name are Nones
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email =="":
            raise forms.ValidationError(
                self.error_messages['email_none'],
                code='email_none',
            )
        return email
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        if first_name =="" or last_name=="":
            raise forms.ValidationError(
                self.error_messages['first_name_none'],
                code='first_name_none',
            )
        return first_name,last_name
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if last_name=="":
            raise forms.ValidationError(
                self.error_messages['last_name_none'],
                code='last_name_none',
            )
        return last_name




