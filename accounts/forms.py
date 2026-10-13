from django import forms
from django.contrib.auth.models import User
from .models import JobSeekerProfile, EmployerProfile


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput
    )

    ROLE_CHOICES = [
        ('jobseeker', 'Job Seeker'),
        ('employer', 'Employer'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password',
        ]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm:

            if password != password_confirm:

                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data