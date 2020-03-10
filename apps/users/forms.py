from django import forms

from apps.users.models import UserProfile
from apps.operations.models import UserFavorite


class DeletUserFavForm(forms.ModelForm):
    class Meta:
        model=UserFavorite
        fields=['user','fav_id','fav_type']

class UpdatePwdForm(forms.Form):
    password1 = forms.CharField(min_length=6,required=True)
    password2 = forms.CharField(min_length=6,required=True)

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 == password2:
            return self.cleaned_data
        raise forms.ValidationError('密码不一致')


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=6)
