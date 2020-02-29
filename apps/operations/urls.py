from django.urls import path
from apps.operations.views import AddFavView

urlpatterns = [
    path('add_fav/', AddFavView.as_view(), name='add_fav'),


]
