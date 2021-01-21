from django import forms
from django.contrib.auth.models import User


messages = {
    'required': 'این فیلد الزامی است',
    'invalid': 'لطفا یک ایمیل معتبر وارد کنید'
}

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username or Email', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'your password'}))


class UserRegistrationForm(forms.Form):
    username = forms.CharField(error_messages=messages, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'your username'}))
    email = forms.EmailField(error_messages=messages, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your email'}))
    password1 = forms.CharField(error_messages=messages, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'your password'}))
    password2 = forms.CharField(error_messages=messages, label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'your password'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.exists():
            raise forms.ValidationError('This user already exists!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2:
            if p1 != p2:
                raise forms.ValidationError('Passwords must match!')
