from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    re_password = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_re_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['re_password']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['re_password']

    def clean_email(self):
        if self.cleaned_data['email']:
            user = User.objects.filter(email=self.cleaned_data['email'])
            if user:
                raise forms.ValidationError(
                    "This email is already in use"
                )
        return self.cleaned_data['email']


class UrlForm(forms.Form):
    real_url = forms.CharField(label='Your url')


class UserLoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password')
