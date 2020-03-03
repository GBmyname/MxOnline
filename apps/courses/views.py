from django.shortcuts import render
from django.views import View

from apps.courses.models import Course
from apps.operations.models import UserFavorite
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class CoursesDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))

        has_fav_org=False
        has_fav_course=False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,
                                            fav_id=course.course_org.id,fav_type=2):
                has_fav_org=True
            if UserFavorite.objects.filter(user=request.user,
                                            fav_id=course_id,fav_type=1):
                has_fav_course=True
        course_users=course.usercourse_set.all()[:3]
        return render(request, 'course-detail.html', {
            'course': course,
            'has_fav_org':has_fav_org,
            'has_fav_course':has_fav_course,
            'course_users':course_users
        })


class CoursesListView(View):
    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        recommend_courses = courses.order_by('-click_nums')[:3]

        sort = request.GET.get('sort', '')
        if sort == 'add_time':
            sort = ''
            courses = courses.order_by('-add_time')
        elif sort == 'hot':
            courses = courses.order_by('-click_nums')
        elif sort == 'students':
            courses = courses.order_by('-students')

        # 配置pure_pagination分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(courses, request=request, per_page=5)

        # 需要特别注意，此时org_list已经不再是QuerySet,将数据库信息封装进了xx.object_list，所以在前端需要修改命名格式
        courses = p.page(page)
        return render(request, 'course-list.html', {
            'sort': sort,
            'courses': courses,
            'recommend_courses': recommend_courses,
            'nav': 'courses',

        })
