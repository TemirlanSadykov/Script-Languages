from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product, Comment

class SignUpForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')


class SignInForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image_url', 'description', 'price']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']