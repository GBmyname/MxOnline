from django.urls import path
from apps.users.views import InfoView,UploadImageView,UpdatePwdView
urlpatterns = [
    # 机构相关
    path('info/', InfoView.as_view(), name='info'),
    path('upload_image/',UploadImageView.as_view(),name='upload_image'),
    path('update_pwd/',UpdatePwdView.as_view(),name='update_pwd'),

    path('courses/', InfoView.as_view(), name='courses'),
    path('fav/', InfoView.as_view(), name='fav'),
    path('message/', InfoView.as_view(), name='message'),

]
