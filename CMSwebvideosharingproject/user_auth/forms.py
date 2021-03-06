from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate,get_user_model)


User=get_user_model()

class UserForm(forms.ModelForm):
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


class UserLoginForm(forms.Form):
    error_messages = {
        'Not_user': ("This user does not exist"),
        'Password_error': ("Incorrect password"),
        'Not_activate': ("This user is not longer active."),
    }
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            if not user:
                raise forms.ValidationError(
                    self.error_messages['Not_user'],
                    code='Not_user',
                )
            if not user.check_password(password):
                raise forms.ValidationError(
                    self.error_messages['Password_error'],
                    code='Password_error',
                )
            if not user.is_active:
                raise forms.ValidationError(
                    self.error_messages['Not_activate'],
                    code='Not_activate',
                )

        return super(UserLoginForm,self).clean()


