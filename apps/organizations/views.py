from django.shortcuts import render
from django.views import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from apps.organizations.models import City, CourseOrg


class OrgListView(View):
    def get(self, request, *args, **kwargs):
        cities = City.objects.all()
        org_list = CourseOrg.objects.all()
        # 配置pure_pagination分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(org_list, request=request, per_page=5)

        # 需要特别注意，此时org_list已经不再是QuerySet,将数据库信息封装进了xx.object_list，所以在前端需要修改命名格式
        org_list = p.page(page)

        return render(request, 'org-list.html', {'cities': cities, 'org_list': org_list})
