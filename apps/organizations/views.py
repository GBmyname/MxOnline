from django.shortcuts import render
from django.views import View
from pure_pagination import Paginator, PageNotAnInteger
from django.http import JsonResponse

from apps.organizations.models import City, CourseOrg, Teacher
from apps.courses.models import Course
from apps.organizations.forms import AddAskForm
from apps.operations.models import UserFavorite


class TeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwargs):
        teacher = Teacher.objects.get(id=teacher_id)
        courses = Course.objects.filter(teacher=teacher)
        classic_courses = courses.filter(is_classic=True)[:3]
        teachers = Teacher.objects.all()
        rank_teacher = teachers.order_by('-fav_nums')

        # request.user.userfavorite_set.fav_id

        teacher_fav = UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type='3')
        org_fav = UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type='2')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(courses, request=request, per_page=2)

        # 需要特别注意，此时org_list已经不再是QuerySet,将数据库信息封装进了xx.object_list，所以在前端需要修改命名格式
        courses = p.page(page)

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'courses': courses,
            'classic_courses': classic_courses,
            'rank_teacher': rank_teacher,
            'teacher_fav': teacher_fav,
            'org_fav':org_fav,

        })


class TeacherListView(View):
    def get(self, request, *args, **kwargs):
        teachers = Teacher.objects.all()
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            teachers = teachers.order_by('-click_nums')
        rank_teacher = teachers.order_by('-fav_nums')

        # 配置pure_pagination分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(teachers, request=request, per_page=2)

        # 需要特别注意，此时org_list已经不再是QuerySet,将数据库信息封装进了xx.object_list，所以在前端需要修改命名格式
        teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'teachers': teachers,
            'rank_teacher': rank_teacher,
            'sort': sort

        })


class TeachersView(View):
    def get(self, request, org_id, *args, **kwargs):
        active = 'teachers'
        org = CourseOrg.objects.get(id=org_id)
        org_has_fav=UserFavorite.objects.filter(user=request.user,fav_id=org.id,fav_type='2')
        return render(request, 'org-detail-teachers.html', {
            'org': org,
            'active': active,
            'org_has_fav':org_has_fav
        })


class DescView(View):
    def get(self, request, org_id, *args, **kwargs):
        active = 'desc'
        org = CourseOrg.objects.get(id=org_id)
        org_has_fav=UserFavorite.objects.filter(user=request.user,fav_id=org.id,fav_type='2')

        return render(request, 'org-detail-desc.html', {
            'org': org,
            'active': active,
            'org_has_fav': org_has_fav

        })


class CoursesView(View):
    def get(self, request, org_id, *args, **kwargs):
        active = 'courses'
        courses = Course.objects.filter(course_org=org_id)
        org = CourseOrg.objects.get(id=org_id)
        org_has_fav=UserFavorite.objects.filter(user=request.user,fav_id=org.id,fav_type='2')

        # 配置pure_pagination分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(courses, request=request, per_page=8)

        # 需要特别注意，此时org_list已经不再是QuerySet,将数据库信息封装进了xx.object_list，所以在前端需要修改命名格式
        courses = p.page(page)

        return render(request, 'org-detail-course.html', {
            'courses': courses,
            'org': org,
            'active': active,
            'org_has_fav': org_has_fav

        })


class HomePageView(View):
    def get(self, request, org_id, *args, **kwargs):
        active = 'homepage'
        org = CourseOrg.objects.get(id=org_id)
        org_has_fav=UserFavorite.objects.filter(user=request.user,fav_id=org.id,fav_type='2')
        return render(request, 'org-detail-homepage.html', {
            'org': org,
            'active': active,
            'org_has_fav':org_has_fav,

        })


class AddAskView(View):
    def post(self, request, *args, **kwargs):
        add_ask_form = AddAskForm(request.POST)
        if add_ask_form.is_valid():
            add_ask_form.save(commit=True)
            return JsonResponse({
                'status': 'success'
            })
        else:
            # 此处由于采用JSON格式传递，所以未将formmodel传递至前端进行显示
            return JsonResponse({
                'status': 'fail',
                'msg': '信息格式有误'
            })


class OrgListView(View):
    def get(self, request, *args, **kwargs):
        cities = City.objects.all()
        org_list = CourseOrg.objects.all()
        hot_list = org_list.order_by('-click_nums')[:3]
        # config filter by category of Org
        category = request.GET.get('ct', '')
        if category:
            org_list = org_list.filter(category=category)
        # config filter by city of Org
        city_id = request.GET.get('city', '')
        if city_id:
            org_list = org_list.filter(city_id=int(city_id))
        # 根据要求进行排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            org_list = org_list.order_by('-students')
        elif sort == 'course_nums':
            org_list = org_list.order_by('-course_nums')

        org_num = org_list.count()

        # 配置pure_pagination分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(org_list, request=request, per_page=5)

        # 需要特别注意，此时org_list已经不再是QuerySet,将数据库信息封装进了xx.object_list，所以在前端需要修改命名格式
        org_list = p.page(page)

        return render(request, 'org-list.html', {
            'cities': cities,
            'org_list': org_list,
            'category': category,
            'city_id': city_id,
            'org_num': org_num,
            'sort': sort,
            'hot_list': hot_list,
            'nav': 'org',
        })
