from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.forms import ModelForm, TextInput, Textarea, CheckboxInput, SelectDateWidget, URLField


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        #model = User
        model = get_user_model()
        #fields = ('username', 'email', 'password1', 'password2')
        fields = ('email', 'nickname', 'password1', 'password2')


class UserUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'nickname', 'twitter_url', 'intro_text')
        labels = {
            'email': 'Emailアドレス',
            'nickname': 'ユーザ名(ニックネーム)',
            'twitter_url': 'Twitter URL(https://twitter.com/の後のIDを入力)',
            'intro_text': '自己紹介',
        }
        # widgets = {
        #     #'status': TextInput(attrs={'class': ''}),
        #     'content': TextInput(attrs={'class': ''}),
        #     'target_date': SelectDateWidget(attrs={'class': ''}),
        #     'publish_set': CheckboxInput(attrs={'class': ''}),
        # }


    #fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff')
    #fields = ('email', 'nickname', 'twitter_url', 'intro_text', 'image')
    #label_tag = ('email':'Emailアドレス','nickname': 'ユーザ名(ニックネーム)','twitter_url':'Twitter URL','intro_text':'自己紹介','image':'画像')
