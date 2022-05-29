from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model, authenticate

CustomUser = get_user_model()

"""
    Taken from this guide: https://www.youtube.com/watch?v=oZUb372g6Do
"""


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'username',
            'id': 'username',
            'type': 'text',
            'placeholder': 'Username',
            'maxlength': '24',
            'minlength': '5',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'placeholder': 'Email',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'password1',
            'id': 'password1',
            'type': 'password',
            'placeholder': 'Password',
            'width': '300px',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'password2',
            'id': 'password2',
            'type': 'password',
            'placeholder': 'Repeat password',
        })

    email = forms.EmailField(help_text="Required")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'password1', 'password2')


class LogInForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'email',
            'id': 'email',
            'type': 'email',
            'placeholder': 'Email',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'required': '',
            'name': 'password',
            'id': 'password',
            'type': 'password',
            'placeholder': 'Password',
        })

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Failed to log in: Validation error")
