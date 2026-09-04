from django import forms
from .models import TechCategory,Technology,Project
from django.utils.text import slugify

class ProjectForm(forms.ModelForm):

  class Meta:
    model = Project
    fields = [
        'title',
        'description',
        'technologies',
        'status',
        'github_url',
    ]
    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'description': forms.Textarea(
            attrs={'class': 'form-control', 'rows': 4}
        ),
        'technologies': forms.SelectMultiple(
            attrs={'class': 'form-control custom-select-multi', 'size': 5}
        ),
        'status': forms.Select(attrs={'class': 'form-control'}),
        'github_url': forms.URLInput(attrs={'class': 'form-control'}),
    }
    


class TechnologyForm(forms.ModelForm):

  class Meta:
    model = Technology
    fields = ['name', 'category', 'proficiency', 'is_learning']
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'category': forms.Select(attrs={'class': 'form-control'}),
        'proficiency': forms.Select(attrs={'class': 'form-control'}),
    }

    
