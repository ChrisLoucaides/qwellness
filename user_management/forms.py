from django import forms
from .models import Account, Advisor


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    advisor = forms.ModelChoiceField(queryset=Advisor.objects.all(), empty_label="Select Advisor")

    class Meta:
        model = Account
        fields = ['username', 'password', 'confirm_password', 'email', 'first_name', 'last_name', 'advisor']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
            'confirm_password': 'Confirm Password',
            'first_name': 'First Name',
            'last_name': 'Last Name'
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Account.Role.STUDENT  # Set role to Student
        if commit:
            user.save()
        return user
