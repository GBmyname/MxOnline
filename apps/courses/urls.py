from django.urls import path
from apps.courses.views import CoursesListView,CoursesDetailView,CourseLessonView,CourseCommentsView,CoursePlayView
from apps.operations.views import AddFavView

urlpatterns = [
    path('list/', CoursesListView.as_view(), name='list'),
    path('detail/<int:course_id>', CoursesDetailView.as_view(), name='detail'),
    path('add_fav/<int:course_id>', AddFavView.as_view(), name='add_fav'),
    path('<int:course_id>/lesson/', CourseLessonView.as_view(), name='lesson'),
    path('<int:course_id>/comment/', CourseCommentsView.as_view(), name='comment'),
    path('<int:course_id>/video/<int:video_id>', CoursePlayView.as_view(), name='video'),

]
