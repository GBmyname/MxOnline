from django.urls import path
from apps.operations.views import AddFavView,AddCommentView

urlpatterns = [
    path('add_fav/', AddFavView.as_view(), name='add_fav'),
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),

]
