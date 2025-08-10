from django import forms
from blog.models import Comment,Ticket

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
