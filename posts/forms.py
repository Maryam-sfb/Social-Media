from django import forms
from posts.models import Post, Comment


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
        error_messages = {
            'body': {
                'required': 'این فیلد الزامی است',
            }
        }
        help_texts = {
            'body': 'Max 400 characters',
        }
        labels = {
            'body': 'Leave a comment',
        }


class AddReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
        }
        error_messages = {
            'body': {
                'required': 'این فیلد الزامی است',
            }
        }
        labels = {
            'body': 'Reply',
        }