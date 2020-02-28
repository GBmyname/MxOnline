from django.urls import path,re_path
from apps.organizations.views import OrgListView,AddAskView,HomePageView

urlpatterns = [
    # 机构相关
    path('list/', OrgListView.as_view(), name='list'),
    path('add_ask/',AddAskView.as_view(),name='add_ask'),
    path('home_page/', HomePageView.as_view(), name='home_page'),
    # path('courses/', HomePageView.as_view(), name='courses'),
    # path('desc/', HomePageView.as_view(), name='desc'),
    # path('teachers/', HomePageView.as_view(), name='teachers'),

]
