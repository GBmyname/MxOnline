from django.urls import path
from apps.courses.views import CoursesListView,CoursesDetailView
from apps.operations.views import AddFavView

urlpatterns = [
    path('list/', CoursesListView.as_view(), name='list'),
    path('detail/<int:course_id>', CoursesDetailView.as_view(), name='detail'),
    path('add_fav/<int:course_id>', AddFavView.as_view(), name='add_fav'),

]
