from django import forms
from django.contrib.auth import get_user_model

from shortener_app.services import form_services

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """
        The form that is needed for user registration.
        Includes some custom field checks.
    """

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    re_password = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password(self):
        password = self.cleaned_data['password']
        username = self.cleaned_data['username']
        if username in password or password in username:
            msg = "Password is very close to username."
            self.add_error('password', msg)
        return password

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
    forbidden_chars = form_services.get_forbidden_url_chars()

    real_url = forms.CharField(label='Long url')

    def clean_real_url(self):
        cd = self.cleaned_data['real_url']
        if cd == '':
            msg = 'Please enter the link.'
            self.add_error('real_url', msg)
        else:
            msg = 'The link does not comply with the service restrictions.'
            for char in self.forbidden_chars:
                if char in cd:
                    self.add_error('real_url', msg)
                    break
        return cd


class UserLoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password')
