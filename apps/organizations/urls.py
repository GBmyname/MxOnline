from django.urls import path
from apps.organizations.views import OrgListView,AddAskView,HomePageView,CoursesView,DescView,TeachersView

urlpatterns = [
    # 机构相关
    path('list/', OrgListView.as_view(), name='list'),
    path('add_ask/',AddAskView.as_view(),name='add_ask'),
    path('homepage/<int:org_id>', HomePageView.as_view(), name='homepage'),
    path('courses/<int:org_id>', CoursesView.as_view(), name='courses'),
    path('desc/<int:org_id>', DescView.as_view(), name='desc'),
    path('teachers/<int:org_id>', TeachersView.as_view(), name='teachers'),

]
