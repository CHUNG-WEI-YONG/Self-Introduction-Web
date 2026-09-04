from django import forms
from django.utils.text import slugify
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'status', 'publish_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., High-Performance C++ Concurrency Patterns'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 12,
                'placeholder': 'Write your full engineering notes here...'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-input'
            }),
            'status': forms.Select(attrs={
                'class': 'form-input'
            }),
            'publish_date': forms.DateTimeInput(attrs={
                'class': 'form-input',
                'type': 'datetime-local'
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.title)
        if commit:
            instance.save()
            self.save_m2m()
        return instance



