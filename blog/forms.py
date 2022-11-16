from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    نام = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'اسم', 'style': 'width: 300px;',
                                                                       'class': 'form-wrap'}))
    ایمیل = forms.EmailField(
        widget=forms.TextInput(
            attrs={'placeholder': 'ایمیل', 'style': 'width: 300px;', 'class': 'form-wrap'}))
    گیرنده = forms.EmailField(
        widget=forms.TextInput(
            attrs={'placeholder': 'گیرنده', 'style': 'width: 300px;', 'class': 'form-wrap'}))
    نظر = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'placeholder': 'نظر دادن', 'style': 'width: 300px;', 'class': 'form-wrap'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
