from django import forms
from django.contrib.auth import (
                authenticate,
                get_user_model
)

from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    username=forms.CharField(label='username', widget=forms.TextInput(attrs={'class':'input100', 'id':'username','placeholder':'Username','name':'username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'input100', 'id':'password','placeholder':'Password','name':'password'}))
    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')

        if username and password:
            user=authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError('user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('user is not active')
        return super(UserLoginForm,self).clean(*args,**kwargs)


class UserRegisterForm(forms.ModelForm):
    username=forms.CharField(label='username', widget=forms.TextInput(attrs={'class':'form-input', 'id':'username','placeholder':'Username'}))
    email=forms.EmailField(label='email',widget=forms.EmailInput(attrs={'class':'form-input', 'id':'email','placeholder':'Your Email'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-input', 'id':'password','placeholder':'Password'}))
    password_confirm=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-input', 'id':'confirm_password','placeholder':'Confirm Password'}))

    class Meta:
        model=User
        fields= [
            'username',
            'email',
            'password',
            'password_confirm'
        ]

        def clean(self):
            email=self.cleaned_data.get('email')
            password=self.cleaned_data.get('password')
            password_confirm=self.cleaned_data.get('password_confirm')
            
            email_qs=User.objects.filter(email=email)
            if email_qs.exists():
                raise forms.ValidationError('email already exists')
            return email
