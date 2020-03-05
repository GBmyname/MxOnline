from django import forms
from apps.operations.models import UserFavorite, CourseComments


class AddFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ['fav_id', 'fav_type']


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ['user','course', 'comments']
