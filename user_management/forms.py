from django import forms
from .models import Account, Advisor


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    advisor = forms.ModelChoiceField(queryset=Account.objects.filter(role=Account.Role.ADVISOR), empty_label="Select Advisor")

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['advisor'].queryset = Advisor.objects.filter(role=Account.Role.ADVISOR)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Account.Role.STUDENT
        if commit:
            user.save()
        return user
