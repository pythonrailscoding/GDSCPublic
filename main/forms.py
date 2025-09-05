from django import forms
from .models import BlogModel, Comment

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['user', 'title', 'content',
                  'thumbnail']

        widgets = {
            'user': forms.TextInput(attrs={'id': 'userid', 'type': 'hidden'}),
            'title': forms.TextInput(attrs={'class': "input", 'placeholder': 'Enter Blog Title'}),
            # 'content': forms.Textarea(attrs={'class':"form-control", 'placeholder': 'Enter Blog Content', 'rows': 10}),
            'thumbnail': forms.FileInput(attrs={"class": "file",
            "accept": "image/*",
            "id": "image"})
        }


class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['user', 'title', 'content',
                  'thumbnail']

        widgets = {
            'user': forms.TextInput(attrs={'id': 'userid', 'type': 'hidden'}),
            'title': forms.TextInput(attrs={'class': "input", 'placeholder': 'Enter Blog Title'}),
            # 'content': forms.Textarea(attrs={'class':"form-control", 'placeholder': 'Enter Blog Content', 'rows': 10}),
            'thumbnail': forms.FileInput(attrs={"class": "file",
            "accept": "image/*",
            "required": "true",
            "id": "image"})
        }


