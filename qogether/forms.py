from django import forms
from .models import Question, Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('question','author', 'title', 'description', 'article_tag', 'header_image')
        widgets = {
            'question': forms.Select(attrs={'class': 'form-control', 'id':'question', 'type':'hidden'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'name', 'type':'hidden'}),
            #'author': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type in some title'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'article_tag': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('question', 'title', 'description', 'article_tag', 'header_image')
        widgets = {
            'question': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type in some title'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'article_tag': forms.TextInput(attrs={'class': 'form-control'}),
        }
