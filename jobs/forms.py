from django import forms
from .models import Job


class JobForm(forms.ModelForm):

    class Meta:
        model = Job

        fields = [
            'title',
            'description',
            'skills_required',
            'location',
            'salary',
            'job_type',
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter job title'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Describe the job',
                    'rows': 5
                }
            ),

            'skills_required': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Python, Django, SQL'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter job location'
                }
            ),

            'salary': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Example: ₹4-6 LPA'
                }
            ),

            'job_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }