from django.urls import path
from apps.users.views import InfoView,UploadImageView,UpdatePwdView,\
    CoursesView,FavTeacherView,FavCoursesView,FavOrgView,MessageView
urlpatterns = [
    # 机构相关
    path('info/', InfoView.as_view(), name='info'),
    path('upload_image/',UploadImageView.as_view(),name='upload_image'),
    path('update_pwd/',UpdatePwdView.as_view(),name='update_pwd'),

    path('courses/', CoursesView.as_view(), name='courses'),
    path('fav/courses', FavCoursesView.as_view(), name='fav_courses'),
    path('fav/teachers', FavTeacherView.as_view(), name='fav_teachers'),
    path('fav/orgs', FavOrgView.as_view(), name='fav_orgs'),
    path('message/', MessageView.as_view(), name='message'),

]
