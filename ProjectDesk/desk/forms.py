from django import forms
from django.core.exceptions import ValidationError
from .models import Post,Comment

class PostForm(forms.ModelForm):
    header = forms.CharField(min_length=5)

    class Meta:
       model = Post
       fields = [
           'header',
           'text',
           'author',
       ]

    def clean(self):
       cleaned_data = super().clean()
       header = cleaned_data.get("header")
       return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text':"введите комментарий"
            }
        widgets = {
            'text': forms.Textarea(attrs={'class':'form-text', 'cols':200,'rows':3}),
        }