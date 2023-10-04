from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'message']

        widgets = {
            'name': forms.TextInput(attrs={"class":"form-control", "id":"name"}),
            'email': forms.EmailInput(attrs={"class":"form-control", "id":"email"}),
            'message': forms.Textarea(attrs={"class":"form-control","cols":"30", "rows":"10", "id":'message'}),
        }

