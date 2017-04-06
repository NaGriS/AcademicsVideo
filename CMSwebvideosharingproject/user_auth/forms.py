from django import forms

class RegisterForm(forms.Form):
    username=forms.CharField(label='User_name',max_length=100)
    password=forms.CharField(widget=forms.PasswordInput)
    email=forms.EmailField(label='Email')