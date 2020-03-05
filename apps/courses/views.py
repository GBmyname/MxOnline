from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.courses.models import Course, CourseTag, Lesson, Video
from apps.operations.models import UserFavorite, UserCourse, CourseComments
from pure_pagination import Paginator, PageNotAnInteger


class CoursePlayView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, video_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        video = Video.objects.get(id=video_id)

        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        # get chapter
        chapters = Lesson.objects.filter(course=course)

        # related_courser
        # tag=course.coursetag_set.
        student_courses = course.usercourse_set.all()
        students_list = [student_course.user for student_course in student_courses]
        relate_courses = UserCourse.objects.filter(user__in=students_list). \
                             exclude(course=course).order_by('course__click_nums')[:2]

        return render(request, 'course-play.html', {
            'course': course,
            'chapters': chapters,
            'relate_courses': relate_courses,
            'video': video,

        })


class CourseCommentsView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        user_comments = CourseComments.objects.filter(course=course).order_by('-add_time')

        return render(request, 'course-comment.html', {
            'course': course,
            'user_comments': user_comments,
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        # get chapter
        chapters = Lesson.objects.filter(course=course)

        # related_courser
        # tag=course.coursetag_set.
        student_courses = course.usercourse_set.all()
        students_list = [student_course.user for student_course in student_courses]
        relate_courses = UserCourse.objects.filter(user__in=students_list). \
                             exclude(course=course).order_by('course__click_nums')[:2]

        return render(request, 'course-video.html', {
            'course': course,
            'chapters': chapters,
            'relate_courses': relate_courses
        })


class CoursesDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_org = False
        has_fav_course = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
            if UserFavorite.objects.filter(user=request.user,
                                           fav_id=course_id, fav_type=1):
                has_fav_course = True

        # related_courser
        # tag=course.coursetag_set.
        tag_list = [tag.tag for tag in CourseTag.objects.filter(course_id=course.id)]
        course_tags = []
        if tag_list:
            course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course_id=course_id)[:3]
        relate_course = set()
        for course_tag in course_tags:
            relate_course.add(course_tag.course)

        return render(request, 'course-detail.html', {
            'course': course,
            'has_fav_org': has_fav_org,
            'has_fav_course': has_fav_course,
            'relate_course': relate_course,
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
