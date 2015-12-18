from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    password1 = forms.CharField(widget=forms.PasswordInput(), max_length=200, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), max_length=200, label="Confirm your Password")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(username__iexact=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("The email you have chosen already exists.")

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You haven't confirmed your password.")
        if password1 != password2:
            raise forms.ValidationError("Your passwords don't match.")
        return password2