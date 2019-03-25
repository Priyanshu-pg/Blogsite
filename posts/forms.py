from django import forms
from .models import SubscribedUsers, Users


class SubscribeUserForm(forms.ModelForm):
    class Meta:
        model = SubscribedUsers
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={
                'id': 'email-text',
                'required': True,
                'placeholder': 'Enter your email'
            }),
        }


class SubscriptionChoiceForm(forms.ModelForm):
    class Meta:
        model = SubscribedUsers
        fields = ['frequency', 'tags_followed']


class UnsubscribeForm(forms.ModelForm):
    class Meta:
        model = SubscribedUsers
        fields = []


class LoginForm(forms.Form):
    email = forms.EmailField(help_text='Enter registered email id', required=True)
    password = forms.CharField(max_length=500, widget=forms.PasswordInput(), label='Enter your password')
    class Meta:
        model = Users
        fields = ['email', 'password']
        widgets = {
            'email': forms.TextInput(attrs={
                'id': 'email-text',
                'required': True,
                'placeholder': 'Enter your email'
            }),
            'password': forms.PasswordInput()
        }


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=500, widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'id': 'first-name-text',
                'required': True,
                'placeholder': 'Enter your first name '
            }),
            'last_name': forms.TextInput(attrs={
                'id': 'last-name-text',
                'required': True,
                'placeholder': 'Enter your last name '
            }),
            'email': forms.TextInput(attrs={
                'id': 'email-text',
                'required': True,
                'placeholder': 'Enter your email'
            }),
            'password': forms.PasswordInput()
        }

        # TODO: this validation should happen on front end side
    def clean_password(self):
        MIN_LENGTH = 8
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        if len(password) < MIN_LENGTH:
            raise forms.ValidationError("Password too short! Must be at least %d char long" % MIN_LENGTH)

        # check for digit
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('Password must contain at least 1 digit.')

        # check for letter
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError('Password must contain at least 1 letter.')

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password == confirm_password:
            return cleaned_data
        else:
            msg = "This doesn't match your password"
            self.add_error('confirm_password', forms.ValidationError(msg))



