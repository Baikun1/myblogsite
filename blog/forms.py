from django import forms
from django.db.models import Max
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import (User, BlogPost, Comment, Category, 
                    ContactSuggestion, Share)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-500'
            })
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'profile_picture', 'bio')
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tell us about yourself...', 'rows': 3})

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category', 'featured_image', 'published']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }

    def save(self, commit=True):
        blog_post = super().save(commit=False)
        if not blog_post.featured_image:
            most_liked_post = BlogPost.objects.filter(category=blog_post.category).order_by('-likes', '-views').first()
            if most_liked_post:
                blog_post.featured_image = most_liked_post.featured_image
            else:
                blog_post.featured_image = f"{settings.STATIC_URL}post/blg.jpg"

        if commit:
            blog_post.save()
        
        return blog_post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ContactSuggestionForm(forms.ModelForm):
    class Meta:
        model = ContactSuggestion
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your message or suggestion...'
            })
        }

class ShareForm(forms.ModelForm):
    class Meta:
        model = Share
        fields = ['platform']
